# Headless GhidraSQL recovery report

## Target and environment

The target was the local `/bin/ls`, copied byte-for-byte before analysis.

| Property | Value |
|---|---|
| Format | ELF 64-bit LSB PIE executable |
| Architecture | x86-64, little-endian |
| State | Dynamically linked, stripped |
| GNU version | coreutils 9.4 |
| Entry point | `0x106D30` |
| Recovered `main` | `0x104DA0` |
| SHA-256 | `0148f5ab3062a905281d8deb9645363da5131011c9e7b6dcaa38b504e41b68ea` |

The completed stack used Ghidra 12.1.2, GhidraSQL 0.0.3, libghidra 0.0.3,
OpenJDK 21.0.12, Gradle 8.14.3, and CMake 3.31.8. The reconstruction was
validated with Ubuntu GCC 13.3.0.

Repository revisions:

- GhidraSQL: `33d5dea43accfe67f4e17a6c7e63e44c053ee47e`
- libghidra: `0afcaa349c7b5d8f60673b64d2093e3f70ef67d7`
- ghidrasql-skills: `73a32759488e6ff208796bdbe59a0d24d7a6cb99`

## Live analysis workflow

GhidraSQL was launched in managed headless mode with an ephemeral local
libghidra RPC port, SQL HTTP service on `127.0.0.1:8081`, a persistent Ghidra
project, and shutdown policy `save`.

The recorded query sequence was:

1. Inventory the binary, functions, call graph, imports, strings, and hot
   functions.
2. Trace `_start` through `__libc_start_main` to recover `main`.
3. Scope decompiler queries by function address and use call/xref/string
   evidence to infer responsibilities.
4. Rename, prototype, plate-comment, and progress-tag 15 high-value functions.
5. Read each target before mutation, verify it after mutation, and call
   `save_database()`.
6. Query the final live revision and annotation count, save, and stop the
   managed server.
7. Reopen the same project read-only and query every recovered function,
   prototype, comment, and tag to prove persistence.

The live database reached program revision 316 before its final save. On
read-only reopen, all 15 annotations were present. The different reopened
revision representation (`3`) is the persisted project database's revision,
not a loss of annotations.

## Recovered structure

The recovered architecture is:

1. Parse options, locale, environment, terminal state, quoting, color, time,
   and output layout.
2. Gather operands and directory entries into an owned file vector.
3. Sort the vector using the selected sort mode and direction.
4. Render the current vector in long, column, row, comma, or single-column
   form.
5. Extract directories into a deferred queue.
6. Enumerate queued directories and optionally enqueue recursive children.

The strongest evidence came from the recovered `main`, the call graph,
embedded GNU help text and `src/ls.c` assertion strings, and individually
scoped decompilation of the gather/sort/render/traversal functions.

## Installation and runtime failures

| Stage | Observed failure | Cause | Resolution |
|---|---|---|---|
| Toolchain discovery | Required JDK 21, modern CMake, and Gradle were absent or unusable from the system path | Host tools did not satisfy the install prompt | Installed workspace-local OpenJDK 21.0.12, CMake 3.31.8, and Gradle 8.14.3 |
| Java loader | `libjli.so: cannot open shared object file` | The relocatable JDK's private libraries were not on the loader path | Supplied the JDK `lib` and `lib/server` directories through `LD_LIBRARY_PATH` |
| Temporary files | Java/native steps could not rely on a normal `/tmp` | The runtime had no usable conventional temporary directory | Used workspace `.tmp` through `TMPDIR` and `-Djava.io.tmpdir` |
| Dependency transport | HTTPS dependency resolution/downloads failed or were interrupted | The environment used restricted/proxied transport and Java trust did not initially match it | Used the available Git transport, resumable downloads, and a workspace-local Java trust setup |
| Parallel native build | The assembler received truncated input during a concurrent build | Resource pressure interrupted a compiler process and left an incomplete assembly stream | Removed only the failed target output and rebuilt serially |
| Ghidra launch | `support/launch.sh` failed where Bash process substitution required `/dev/fd` | `/dev/fd` was unavailable in the runtime | Replaced the two process-substitution loops with command-substitution here-strings and empty-line guards |
| First managed GhidraSQL run | glibc aborted in `pthread_mutex_lock` | Two cpp-httplib revisions/configurations were linked into one executable: fastmcpp's `cpp_httplib` and the top-level `httplib`, with different OpenSSL/zlib feature macros and therefore incompatible inline class layouts | Forced fastmcpp's FetchContent declaration to reuse the top-level cpp-httplib source and linked `fastmcpp_core` publicly to `httplib::httplib` |
| First strict recovered-source build | Fallthrough and “control reaches end” diagnostics became errors | The compiler did not know that `usage()` and the out-of-memory handler never return | Marked both helpers `_Noreturn`; the final strict build is clean |

The CMake fix is the material upstream source change. The Ghidra launch patch
is an environment-specific compatibility patch.

A non-fatal Ghidra FileStore warning appeared for
`/var/tmp/root-ghidra/fscache2`. It did not prevent project creation, analysis,
saves, clean shutdown, or read-only reopen.

## Validation

- Exact target copy: source and captured binary SHA-256 hashes match.
- Headless live project: 412 functions, 79,542 bytes in functions, 1,363
  callgraph edges, 259 string references.
- Mutations: 15 functions named, prototyped, commented, and tagged.
- Save: final `save_database()` returned `1`.
- Shutdown: managed server exited `0`.
- Persistence: read-only reopen returned all 15 annotations; readonly server
  exited `0`.
- Source cleanliness: no `FUN_`, `DAT_`, `LAB_`, decompiler `undefinedN`
  types, or decompiler warning comments occur in `recovered_ls.c`.
- Strict source build: C11 with `-Wall -Wextra -Wpedantic -Werror` succeeded.
- Behavioral smoke test: `--version`, numeric long listing, and single-column
  directory listing succeeded.
- Deterministic comparison: system `/bin/ls -1A --color=never` and
  `recovered-ls -1A --color=never` produced identical names and order for the
  source directory; the diff was empty.

## Reconstruction limits

`recovered_ls.c` is a clean behavioral reconstruction, not a claim to
the original GNU implementation. It intentionally leaves out advanced GNU
features whose exact reimplementation would require substantially more type,
global, locale, and library recovery: full quoting styles, complete
`LS_COLORS`, ACL/SELinux columns, dired offsets, hyperlinks, locale-aware
display widths, version sorting, and every option alias.

Raw Ghidra pseudocode was retained in the query transcript for auditability. The
recovered source itself contains none of those decompiler artifacts.
