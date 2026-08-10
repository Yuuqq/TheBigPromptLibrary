# Full system inventory of the ChatGPT Work VM

*By **Elias Bachaalany** — [@0xeb](https://github.com/0xeb) on GitHub · [Binary Wizards](https://www.youtube.com/@binary-wizards) on YouTube · [@eliasbchlny](https://x.com/eliasbchlny) on X*

ChatGPT Work mode gives you a **VM** — a real Linux machine sitting behind the chat box, not a scratch pad that draws a chart and forgets it. You can write code in it, build that code, browse the web, run experiments, serve files, and keep a persistent filesystem for the length of your session.

That combination is what makes it powerful. Point it at a repository and it will clone it, build it, run the output, and iterate on experiments with you. When you are done, ask it to zip the results and it hands you a download link. A full develop-build-run-collect loop, driven in plain English.

So the obvious question is: **what is the machine?** How many cores, how much RAM, how much disk, which toolchains are already installed, and where are the walls? This is the full inventory — CPU, memory, storage, resource limits, installed software, Python and Node package lists, and the parts of the host the sandbox deliberately refuses to show you.

This article is a companion to the two earlier sandbox inventories in this repo, the [Python package list](./chatgpt-code-python-pkglist-08232024.md) and the [Linux package list](./chatgpt-code-pkglist-08232024.md) of the ChatGPT code interpreter — but that was a different, far more constrained box, and this one goes well past packages.
*Captured **2026-08-06 09:13:48 PDT** (`2026-08-06T16:13:48.374439+00:00`) on a pristine workspace — nothing cloned, installed, or built beforehand. Every figure below is a live reading taken at that moment, not the model's recollection of its own environment.*

## Practical capacity, up front

If you are sizing up what to run in this thing, the useful limits are:

- **9 logical vCPUs**
- **23.55 GB total RAM**, with **22.11 GB free** at capture
- **58.28 GB workspace storage available**
- **No swap**
- Strong Python, Node.js, C/C++, document, spreadsheet, PDF, image, OCR, and media-processing support
- **No** Docker/Podman, Go, Rust, .NET, CMake, Kubernetes, or database client tooling preinstalled

The environment suits moderately large Python/Node projects and Make-based C/C++ projects, subject to the restricted network and sandbox filesystem. Anything that expects CMake, a Go/Rust toolchain, or a container runtime will need to bring it along — or will simply not build.

The rest of this article is the evidence behind those numbers.

## Important scope note

This is a restricted, KVM-backed execution environment. The figures below describe resources exposed **to this workspace**, not the full physical host. `/proc`, `/sys`, the mount table, the Debian package database, PCI devices, and GPU devices are hidden or incomplete. Where ordinary tools could not read those interfaces, the inventory falls back to direct operating-system syscalls and runtime APIs — which is why you will see `sysinfo`-style numbers instead of `free`/`lscpu` output.

## Operating system

| Item | Value |
|---|---|
| Distribution | Ubuntu 24.04.3 LTS |
| Codename | Noble Numbat |
| Kernel | Linux 6.18.35 |
| Kernel build | `#1 SMP Mon Jul 27 18:07:50 UTC 2026` |
| Architecture | x86_64 / AMD64 |
| Word size | 64-bit |
| Byte order | Little-endian |
| C library | glibc 2.39 |
| Virtualization | KVM |
| Hostname | `f20c423af0c2` |
| Workspace time zone | America/Los_Angeles |
| Page size | 4,096 bytes |
| Uptime at capture | 44,515 seconds (~12 h 21 m 55 s) |
| Load averages | 0.000 / 0.000 / 0.000 |
| Process count reported by `sysinfo` | 213 |

Note the container-style hostname and the ~12 hours of uptime on a completely idle box — this workspace had been sitting warm long before I asked it anything.

## CPU

| Item | Value |
|---|---|
| Assigned processors | 9 logical vCPUs |
| CPU affinity | IDs 0 through 8 |
| Exposed architecture generation | AMD Zen 4 |
| Native GCC target | `znver4` |
| CPUID brand reading | AMD EPYC 9V74 80-Core Processor |
| Hypervisor | KVM |
| L1 instruction cache | 32 KiB |
| L1 data cache | 32 KiB |
| Cache-line size | 64 bytes |
| L2 cache | 1 MiB |
| L3 cache | 32 MiB |

The processor brand describes the **virtualized host CPU class**, not your allocation. This workspace has **9 vCPUs**, not 80 dedicated cores. Physical sockets, physical-core count, topology, and frequency are not exposed. The fresh native compiler probe still reports the `znver4` target.

The `AMD EPYC 9V74` string is itself a small tell: the `V` series parts are Azure-specific SKUs, which is consistent with where this workload is hosted.

Exposed native instruction support includes MMX, SSE through SSE4.2, AVX, AVX2, FMA, BMI1/2, AES, PCLMUL, VAES, VPCLMULQDQ, SHA, GFNI, RDRAND, RDSEED, and multiple AVX-512 extensions: F, VL, BW, DQ, CD, VBMI, VBMI2, IFMA, VNNI, VPOPCNTDQ, BITALG, and BF16.

## Memory

Values are dynamic and reflect this capture.

| Item | Size |
|---|---:|
| Total RAM | 23.55 GB |
| Free RAM | 22.11 GB |
| Shared memory | 108 MB |
| Buffer memory | 78 MB |
| Swap total | 0 |
| Swap free | 0 |

**No swap.** Whatever you run here either fits in RAM or gets killed.

## Workspace storage

This is the mounted workspace filesystem capacity, not the host's complete physical storage inventory.

| Item | Size |
|---|---:|
| Filesystem capacity | 67.05 GB |
| Used | 5.32 GB |
| Available to workspace | 58.28 GB |
| Raw free blocks | 61.73 GB |

- Used portion of total capacity: approximately 7.93%.
- Filesystem block and fragment size: 4 KiB.
- Inodes: 4,194,304 total; 4,081,122 free.
- Maximum filename length: 255 bytes.

## Resource limits

| Limit | Soft | Hard |
|---|---:|---:|
| Open files | 16,384 | 16,384 |
| Processes | 7,851 | 7,851 |
| Stack | 8 MiB | Unlimited |
| Core dump | 0 (disabled) | Unlimited ceiling |

## Main development software

| Software | Version | Executable/status |
|---|---|---|
| Git | 2.51.1 | `/usr/local/bin/git` |
| Git LFS | 3.4.1 | `/usr/bin/git-lfs` |
| GCC | 13.3.0 | `/usr/bin/gcc` |
| G++ | 13.3.0 | `/usr/bin/g++` |
| GNU Make | 4.3 | `/usr/bin/make` |
| Python | 3.12.13 | Bundled primary runtime |
| pip | 26.0.1 | Bundled primary runtime |
| uv | 0.11.33 | Bundled primary runtime |
| Node.js | 24.14.0 LTS ("Krypton") | Bundled primary runtime |
| npm | 11.9.0 | Bundled primary runtime |
| pnpm | 11.7.0 | Bundled primary runtime |
| Corepack | 0.34.6 | Globally installed with Node |
| Perl | 5.38.2 | `/usr/bin/perl` |
| Bash | 5.2.21 | `/usr/bin/bash` |
| Zsh | 5.9 | `/usr/bin/zsh` |
| curl | 8.5.0 | `/usr/bin/curl` |
| wget | 1.21.4 | `/usr/bin/wget` |
| OpenSSH | 9.6p1 | `/usr/bin/ssh` |
| OpenSSL CLI | 3.0.13 | `/usr/bin/openssl` |
| apt | 2.8.3 | `/usr/bin/apt` |
| dpkg | 1.22.6 | `/usr/bin/dpkg` |
| jq | 1.7 | `/usr/bin/jq` |
| ripgrep | 15.2.0 | Bundled Codex path |
| nano | Present | `/usr/bin/nano` |
| rsync | Present | `/usr/bin/rsync` |

The bundled Python and Node runtimes use OpenSSL 3.5.5. Python reports SQLite 3.50.4 and zlib 1.3.1. Node reports SQLite 3.51.2, V8 13.6.233.17-node.41, ICU 78.2, Unicode 17.0, libuv 1.51.0, zlib 1.3.1, and zstd 1.5.7.

## Document, image, media, and OCR software

| Software | Version/status |
|---|---|
| FFmpeg | 6.1.1 |
| ImageMagick | 6.9.12-98 Q16 |
| Pandoc | 3.1.3 |
| Tesseract OCR | 5.3.4 |
| Poppler `pdftotext` | 24.02.0 |
| Ghostscript | 10.02.1 |
| LibreOfficeDev | 26.8.0.0.alpha0 (bundled launcher works for version inspection) |
| Inkscape | Executable present, but fails — `libinkscape_base.so` unavailable |
| Java | Launcher present, but fails — `libjli.so` unavailable |

## Installed Python packages

51 installed Python distributions:

```text
PyMuPDF==1.26.6
PyYAML==6.0.3
annotated-types==0.7.0
artifact_tool_v2==2.8.21
cffi==1.17.1
charset-normalizer==3.4.4
contourpy==1.3.3
cryptography==46.0.0
cycler==0.12.1
et_xmlfile==2.0.0
fonttools==4.61.1
joblib==1.5.3
kiwisolver==1.4.9
lxml==6.0.2
matplotlib==3.10.8
numpy==2.3.5
openpyxl==3.1.5
packaging==26.2
pandas==2.2.3
pdf2image==1.17.0
pdfminer.six==20251107
pdfplumber==0.11.8
pillow==12.2.0
pip==26.0.1
pycparser==2.23
pydantic==2.13.4
pydantic_core==2.46.4
pyhumps==3.8.0
pyparsing==3.3.2
pypdf==6.10.0
pypdfium2==5.3.0
python-dateutil==2.9.0.post0
python-docx==1.2.0
python-pptx==1.0.2
pytz==2026.2
reportlab==4.4.9
scikit-learn==1.8.0
scipy==1.17.0
seaborn==0.13.2
setuptools==82.0.1
six==1.17.0
threadpoolctl==3.6.0
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2026.2
uv==0.11.33
websockets==16.0
wheel==0.47.0
xlrd==2.0.1
xlsxwriter==3.2.9
zstandard==0.25.0
```

Compare this with the [2024 code interpreter list](./chatgpt-code-python-pkglist-08232024.md): that sandbox shipped hundreds of packages including the full scientific/ML stack. This one is a *lean* 51 — document processing, plotting, and a minimal scikit-learn/scipy core. Note the internal `artifact_tool_v2==2.8.21` distribution, which is not a public PyPI package.

## Bundled Node.js libraries

Top-level runtime modules:

```text
@napi-rs
@oai
@viz-js
docx
jpeg-js
lucide
marked
pdf-lib
pdfjs-dist
pixelmatch
playwright
pngjs
pnpm
pptxgenjs
sharp
tesseract.js
```

There are 117 `package.json` manifests across the bundled Node dependency tree. Global Node packages are `corepack@0.34.6` and `npm@11.9.0`. The `@oai` scope is, again, internal tooling rather than anything published.

## Software availability summary

Present and usable or discoverable on `PATH`:

```text
apt, dpkg, git, git-lfs, curl, wget, rsync, ssh, scp,
gcc, g++, make, python3, pip, uv, node, npm, npx, pnpm,
perl, jq, rg, nano, ffmpeg, convert, pandoc, soffice,
tesseract, pdftotext, gs
```

Not found as command-line executables:

```text
rpm, apk, snap, flatpak, gh, svn, hg, gfortran, clang,
clang++, cmake, ninja, meson, autoconf, automake, yarn,
bun, deno, ruby, gem, javac, go, rustc, cargo, dotnet,
php, R, sqlite3, psql, mysql, redis-cli, docker, podman,
buildah, kubectl, helm, terraform, ansible, yq, fd, vim,
nvim, emacs, tmux, screen, magick, chromium,
chromium-browser, google-chrome, playwright CLI, qpdf,
nvidia-smi, rocminfo, lspci, lsusb
```

Although a `playwright` Node module is bundled, there is no standalone `playwright` executable on the inspected `PATH`.

## Inventory counts

| Category | Count |
|---|---:|
| Unique executable files found across `PATH` directories | 1,023 |
| Resolvable shell command names | 1,393 |
| Shared libraries in the linker cache | 505 |
| Python distributions | 51 |
| Node package manifests in bundled dependency tree | 117 |

## Visibility limitations

This is the interesting half of the exercise — what the sandbox *won't* tell you:

- The Debian package manager executables exist, but the sandbox does not expose a complete package database. An authoritative full `apt`/`dpkg` package list **cannot** be generated here — which is exactly the trick that worked on the [2024 code interpreter sandbox](./chatgpt-code-pkglist-08232024.md) and no longer works on this one.
- `/proc` and `/sys` are not normally mounted for shell tools, so `lscpu`, `free`, `df`, `lsblk`, and similar utilities cannot produce their usual reports. Direct syscall/runtime readings were used instead.
- GPU presence cannot be confirmed. Neither NVIDIA nor AMD GPU utilities are installed, and PCI/sysfs discovery is unavailable. Read this as **GPU unknown**, not definitively "no GPU."
- Physical disk devices, storage model, RAID layout, CPU sockets, physical-core topology, thermal state, and clock frequency are not exposed.
- Installed executables are not guaranteed to be *functional*. Java and Inkscape are both present launchers with missing runtime libraries.
