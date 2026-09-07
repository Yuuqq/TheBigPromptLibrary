# Code Review: Yuuqq/TheBigPromptLibrary

This review covers the repository architecture, security, reliability, testing, performance, and documentation.

## 1. Security Issues (Injection, Secrets, Authz, Unsafe Defaults)

### HIGH: Unsafe HTML Fallback when `DOMPurify` is Missing
* **File:** `docs/index.html` (lines ~2056-2063)
* **Impact:** The code checks `if (typeof DOMPurify !== 'undefined')` and if it is, sanitizes the markdown HTML. However, the `else` branch directly executes `el.innerHTML = html;`. If the `DOMPurify` CDN fails to load (e.g., due to network issues or ad-blockers), the app "fails open" and will render raw, unsanitized HTML parsed from GitHub markdown files. Since content comes from a public repository, a maliciously crafted markdown file (or MITM on the raw content) could result in Stored XSS.
* **Fix Suggestion:** Fail closed. Change the `else` branch to assign text instead (`el.textContent = content;`) or show an error message explicitly stating that the sanitizer failed to load. Do not insert unsanitized `html` into `innerHTML`.

### MEDIUM: Cross-Site Scripting (XSS) Risks via Unescaped Template Literals
* **File:** `docs/index.html`
* **Impact:** Throughout `docs/index.html`, template literals are used extensively to construct HTML components (e.g., `item.innerHTML = ...`). While `escHtml()` is used in many places, there are potential gaps. For instance, `qsBadge(p.qs)` concatenates directly into `search-result-title`, and some variables derived from external data might bypass escaping if not strictly enforced.
* **Fix Suggestion:** For simple elements that don't need rich HTML (like search result titles or file names), prefer using `element.textContent` instead of building HTML strings and setting `innerHTML`. Where `innerHTML` must be used, audit every variable interpolation to ensure it is wrapped in `escHtml()`.

## 2. Reliability / Error Handling / Edge Cases

### MEDIUM: Provider Fallback Logic May Crash Unpredictably
* **File:** `scripts/translate.py` (lines ~236-250)
* **Impact:** The `call_llm` function iterates through a `PROVIDER_CHAIN`. It catches a generic `Exception` and moves to the next provider. If all providers fail (e.g., due to rate limits or missing API keys), it raises a `RuntimeError` and terminates the script entirely. If this happens mid-run, it fails the GitHub Action immediately without saving partial progress.
* **Fix Suggestion:** Implement exponential backoff for rate-limit exceptions (`HTTP 429`) before immediately failing a provider. Additionally, consider catching only specific request-related exceptions rather than base `Exception`, to avoid masking deeper programming errors (like `KeyError`).

### LOW: Caching Strategy Edge Case for Large Index Files
* **File:** `docs/sw.js` (lines ~20-40)
* **Impact:** The service worker uses a `stale-while-revalidate` strategy for `raw.githubusercontent.com`, which includes the `prompts_index.json`. This file is large (almost 700KB). A user might see a noticeably outdated index for a session if they navigate away before the revalidate completes, and there is no UI indicator that the background refresh is happening or finished.
* **Fix Suggestion:** Add a mechanism to notify the frontend when a new `prompts_index.json` has been successfully fetched and cached, so the UI can prompt the user to "Refresh to see new prompts."

## 3. Architecture and Code Organization Quality

### LOW: Monolithic Frontend File
* **File:** `docs/index.html`
* **Impact:** The `index.html` file is over 3,000 lines long, combining structure (HTML), presentation (CSS), and complex logic (JavaScript) into a single file. This negatively impacts readability, makes git conflicts more likely, and complicates debugging.
* **Fix Suggestion:** Refactor the codebase by extracting the inline CSS into a `styles.css` file and the inline JavaScript into an `app.js` (or module-based scripts) file.

## 4. Test Coverage Gaps and High-Risk Untested Paths

### MEDIUM: Test Suite Fails Due to Brittle Imports and Missing Setup
* **File:** `scripts/test_scripts.py`
* **Impact:** The test file uses `_load(name)` to dynamically load python scripts using `importlib`. The test `test_translate_helpers` crashes with an `AttributeError` (`module 'translate' has no attribute 'MODEL'`) because the implementation in `translate.py` was refactored (now using `PROVIDER_CHAIN`), but the tests were not updated. Consequently, the core LLM translation logic is not actively tested.
* **Fix Suggestion:** Update `test_scripts.py` to match the current `translate.py` implementation. Avoid using brittle `importlib` manual loading; instead, structure the `scripts/` directory as a proper package (add `__init__.py`) so modules can be imported normally (e.g., `import scripts.translate as tr`).

### MEDIUM: Critical Missing Test Coverage for Diff-Translation
* **File:** `scripts/translate.py`
* **Impact:** The script employs complex logic for "Diff-based translation" using paragraph hashing. There are no tests covering this behavior. If a bug is introduced where paragraph alignment fails, it could result in silently skipping translations or triggering full re-translations of every file, which is expensive.
* **Fix Suggestion:** Introduce unit tests that mock the upstream GitHub API and local translation memory (`stats/translation_memory.json`) to verify that the diffing logic correctly isolates and translates only changed paragraphs.

## 5. Documentation and Developer-Experience Gaps

### LOW: Missing Dependency Specification for Local Development
* **File:** Repository Root
* **Impact:** There is no `requirements.txt`, `Pipfile`, or `pyproject.toml` in the repository root. A new developer trying to run `scripts/translate.py` or the test suite locally has to guess the required packages (e.g., `requests`, `pytest`, `PyYAML`). The GitHub Actions workflow (`sync-and-translate.yml`) hardcodes `pip install requests`.
* **Fix Suggestion:** Add a standard `requirements.txt` listing `requests`, `pytest`, and any other required libraries to streamline developer onboarding.
