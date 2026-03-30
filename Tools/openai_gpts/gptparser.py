"""
GPT parsing module.

The GPT markdown files have to adhere to a very specific format described in the README.md file in the root of the CSP project.
"""

import os, re, unicodedata
from collections import namedtuple
from typing import Union, Tuple, Generator, Iterator


GPT_BASE_URLS = ('https://chat.openai.com/g/g-', 'https://chatgpt.com/g/g-')
GPT_BASE_URLS_L = [len(url) for url in GPT_BASE_URLS]
FIELD_PREFIX = 'GPT'

GPT_FILE_ID_RE = re.compile(r'^([0-9a-z]{9})_(.*)\.md$', re.IGNORECASE)
"""GPT file name regex with ID and name capture."""
GPT_FILE_VERSION_RE = re.compile(r'\[([^]]*)\]\.md$', re.IGNORECASE)
"""GPT file name regex with version capture."""

GptFieldInfo = namedtuple('FieldInfo', ['order', 'display'])

GptIdentifier = namedtuple('GptIdentifier', ['id', 'name'])
"""Description of the fields supported by GPT markdown files."""

SUPPORTED_FIELDS = {
    'url':              GptFieldInfo(10, 'URL'),
    'title':            GptFieldInfo(20, 'Title'),
    'description':      GptFieldInfo(30, 'Description'),
    'logo':             GptFieldInfo(40, 'Logo'),
    'verif_status':     GptFieldInfo(50, 'Verification Status'),
    'instructions':     GptFieldInfo(60, 'Instructions'),
    'actions':          GptFieldInfo(70, 'Actions'),
    'kb_files_list':    GptFieldInfo(80, 'KB Files List'),
    'extras':           GptFieldInfo(90, 'Extras'),
    'protected':        GptFieldInfo(100, 'Protected'),
}
"""
Dictionary of the fields supported by GPT markdown files:
- The key should always be in lower case
- The GPT markdown file will have the form: {FIELD_PREFIX} {key}: {value}
"""

FIELD_ALIASES = {
    'url': {
        'url',
        'link',
        '链接',
    },
    'title': {
        'title',
        '标题',
    },
    'description': {
        'description',
        '描述',
    },
    'logo': {
        'logo',
        '图标',
    },
    'verif_status': {
        'verification status',
        'verificationstatus',
        'verification',
        'verif_status',
    },
    'instructions': {
        'instruction',
        'instructions',
        '指令',
        'instructions english',
        'instructions in english',
        'instructions (english)',
        'instructions (unverified)',
        '指令（英文版）',
        '指令（英文）',
    },
    'actions': {
        'action',
        'actions',
        'actions list',
        'actions endpoint',
        'tools',
        'tools/actions',
        '动作',
        '工具/actions',
        'endpoints',
    },
    'kb_files_list': {
        'kb',
        'kb files',
        'kb files list',
        'knowledge files',
        '知识库文件',
        '知识库文件列表',
    },
    'extras': {
        'extra',
        'extras',
        'comments',
        'details',
        'functional summary details',
        'maker',
        'for organized crime historical exploration custom instructions',
    },
    'protected': {
        'protected',
        '受保护',
    },
}


def normalize_field_label(label: str) -> str:
    """Normalize field labels to a punctuation-insensitive lookup key."""
    return ''.join(
        ch.casefold()
        for ch in label
        if not unicodedata.category(ch).startswith(('P', 'Z'))
    )


FIELD_LABEL_LOOKUP = {}
for key, info in SUPPORTED_FIELDS.items():
    FIELD_LABEL_LOOKUP[normalize_field_label(key)] = key
    FIELD_LABEL_LOOKUP[normalize_field_label(info.display)] = key
    for alias in FIELD_ALIASES.get(key, ()):
        FIELD_LABEL_LOOKUP[normalize_field_label(alias)] = key


def resolve_field_label(label: str) -> Union[str, None]:
    """Resolve a markdown field label to a supported GPT field key."""
    normalized = normalize_field_label(label)
    if not normalized:
        return None

    if normalized in FIELD_LABEL_LOOKUP:
        return FIELD_LABEL_LOOKUP[normalized]

    if normalized.startswith('instructions') or '指令' in normalized:
        return 'instructions'
    if normalized.startswith('kbfiles') or normalized.startswith('知识库文件'):
        return 'kb_files_list'
    if normalized in {'kb', '知识库文件'}:
        return 'kb_files_list'
    if normalized.startswith('actions') or normalized.startswith('toolsactions') or normalized.startswith('工具actions'):
        return 'actions'
    if normalized in {'tools', 'endpoints', '动作'}:
        return 'actions'
    if normalized.startswith('verification') or normalized.startswith('verif'):
        return 'verif_status'
    if normalized.startswith('protected') or normalized == '受保护':
        return 'protected'
    if normalized.startswith('extra') or normalized in {'comments', 'details', 'maker', 'functionalsummarydetails'}:
        return 'extras'

    return None

class GptMarkdownFile:
    """
    A class to represent a GPT markdown file.
    """
    def __init__(self, fields=None, filename: str = '') -> None:
        self.fields = fields or {}
        self.filename = filename

    def get(self, key: str, strip: bool = True) -> Union[str, None]:
        """
        Return the value of the field with the specified key.
        :param key: str, key of the field.
        :return: str, value of the field.
        """
        key = key.lower()
        if key == 'version':
            m = GPT_FILE_VERSION_RE.search(self.filename)
            return m.group(1) if m else ''

        v = self.fields.get(key)
        return v.strip() if strip else v
    
    def id(self) -> Union[GptIdentifier, None]:
        """
        Return the GPT identifier.
        :return: GptIdentifier object.
        """
        if gpt_identifier := parse_gpturl(self.fields.get('url')):
            return gpt_identifier

        basename = os.path.basename(self.filename)
        if m := GPT_FILE_ID_RE.match(basename):
            return GptIdentifier(m.group(1), '')
        return None
            
    def __str__(self) -> str:
        sorted_fields = sorted(self.fields.items(), key=lambda x: SUPPORTED_FIELDS[x[0]].order)
        # Check if the field value contains the start marker of the markdown block and add a blank line before it
        field_strings = []
        for key, value in sorted_fields:
            if value:
                # Only replace the first occurrence of ```markdown
                modified_value = value.replace("```markdown", "\r\n```markdown", 1)
                field_string = f"{FIELD_PREFIX} {SUPPORTED_FIELDS[key].display}: {modified_value}"
                field_strings.append(field_string)
        return "\r\n".join(field_strings)

    @staticmethod
    def parse(file_path: str) -> Union['GptMarkdownFile', Tuple[bool, str]]:
        """
        Parse a markdown file and return a GptMarkdownFile object.
        :param file_path: str, path to the markdown file.
        :return: GptMarkdownFile if successful, otherwise a tuple with False and an error message.
        """
        if not os.path.exists(file_path):
            return (False, f"File '{file_path}' does not exist.")

        with open(file_path, 'r', encoding='utf-8') as file:
            fields = {key.lower(): [] for key in SUPPORTED_FIELDS.keys()}
            field_re = re.compile(rf"^\s*{re.escape(FIELD_PREFIX)}\s+(.+?)\s*[:：]\s*", re.IGNORECASE)
            current_field = None
            for line in file:
                if m := field_re.match(line):
                    label = m.group(1).strip()
                    current_field = resolve_field_label(label)
                    line = line[m.end():].lstrip().rstrip('\r\n')

                    if current_field is None:
                        current_field = 'extras'
                        line = f"{label}: {line}\n" if line else f"{label}:\n"

                if current_field:
                    if current_field not in SUPPORTED_FIELDS:
                        return (False, f"Field '{current_field}' is not supported.")

                    fields[current_field].append(line)

        gpt = GptMarkdownFile(
            {key: ''.join(value) for key, value in fields.items()},
            filename=file_path)
        return (True, gpt)

    def save(self, file_path: str) -> Tuple[bool, Union[str, None]]:
        """
        Save the GptMarkdownFile object to a markdown file.
        :param file_path: str, path to the markdown file.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(self))
            return (True, None)
        except Exception as e:
            return (False, f"Failed to save file '{file_path}': {e}")

def parse_gpturl(url: str) -> Union[GptIdentifier, None]:
    for GPT_BASE_URL, GPT_BASE_URL_L in zip(GPT_BASE_URLS, GPT_BASE_URLS_L):
        if url and url.startswith(GPT_BASE_URL):
            id = url[GPT_BASE_URL_L:].split('\n')[0].split('/')[0]
            i = id.find('-')
            if i != -1:
                return GptIdentifier(id[:i], id[i+1:])
            else:
                return GptIdentifier(id, '')
    return None


def get_prompts_path() -> str:
    """Return the path to the Custom GPTs prompts directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'CustomInstructions', 'ChatGPT'))

def enum_gpts() -> Generator[Tuple[bool, Union[GptMarkdownFile, str]], None, None]:
    """Enumerate all the GPT files in the prompts directory, parse them and return the parsed GPT object."""
    prompts_path = get_prompts_path()
    for file_path in os.listdir(prompts_path):
        _, ext = os.path.splitext(file_path)
        if ext != '.md':
            continue
        file_path = os.path.join(prompts_path, file_path)
        ok, gpt = GptMarkdownFile.parse(file_path)
        if ok:
            yield (True, gpt)
        else:
            yield (False, f"Failed to parse '{file_path}': {gpt}")

def enum_gpt_files() -> Iterator[Tuple[str, str]]:
    """
    Enumerate all the GPT files in the prompts directory while relying on the files naming convention.
    To normalize all the GPT file names, run the `idxtool.py --rename`
    """
    prompts_path = get_prompts_path()
    for file_path in os.listdir(prompts_path):
        m = GPT_FILE_ID_RE.match(file_path)
        if not m:
            continue
        file_path = os.path.join(prompts_path, file_path)
        yield (m.group(1), file_path)
