# Workbook verification — 20 November 2026

## Executed locally

| Check | Actual result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 tests/check.py` | PASS: ideal DC divider (6 V), source current (-2 mA), current-source sign (2 V), 361 resistor-ratio cases, 11 rejection fixtures; JSON Schema Draft 2020-12 schema/fixture validation; 406 unique kernel ledger entries; all SVG XML parsed; offline AI broker policy checks |
| `python3 tools/elektra_ref.py examples/elektra/divider.elek` | PASS: vin=8 V, out=6 V, ground=0 V, source current=-0.002 A, scaled residual=0.0 |
| `cmake -S sdk -B /tmp/amb3r-sdk-wb -DCMAKE_BUILD_TYPE=Debug; cmake --build /tmp/amb3r-sdk-wb; ctest --test-dir /tmp/amb3r-sdk-wb --output-on-failure` | PASS: strict native C11, 1/1 CTest; ABI mismatch, insufficient grant, duplicate registration rollback, stale snapshot, valid command, post-shutdown denial |
| `clang -std=c11 -Wall -Wextra -Wpedantic -Werror -fsanitize=address,undefined -fno-omit-frame-pointer -I sdk/include sdk/examples/host.c sdk/examples/plugin.c -o /tmp/amb3r-sdk-san; ASAN_OPTIONS=detect_leaks=1 /tmp/amb3r-sdk-san` | PASS: reference SDK with address/undefined/leak detection enabled; no reported errors |
| Graphviz render | Seven `.dot` files rendered to SVG; two additional hand-authored vector diagrams |

A preliminary reference test run failed because chained string replacement modified the first resistor a second time for one ratio. The test was corrected to target component terminals, then rerun successfully. This was a fixture construction error, not a solver failure.

## Not executed

- MuLIB-dependent C examples: actual selected upstream API signatures inspected through GitHub, but the checkout was not available in the execution container; direct download failed due to inaccessible DNS. Compile using chapter 14 against the pinned revision and adapt names if upstream changed. No MuLIB regression run was performed here.
- On1x source candidates: no on1xc executable available in the container. Proposed On1x resources and PPX examples intentionally not executable yet.
- Full Elektra syntax, HDL/HWIL/Vienna proposals, Lua/Mune host adapter, dynamic/isolated native plugins, project storage and full simulation are design specifications, not implemented in the workbook. The C SDK is a trusted linked, one-command reference only.
- No external simulator/oracle, live hardware, native GPU, hosted LLM request, OpenCode session or local-model inference was tested. The AI mock checks local policy only, not a security audit. JSON Schema validation does not establish semantic validation.
- Recorded upstream tests are historical repository reports, not this workbook's tests. The ledger is a selected tree inventory plus limited source inspection, not an audit of 406 kernels or safe admission.

Run the included self-contained reference tests offline before extending them. Maintain separate statuses for production features and bounded executable references.
