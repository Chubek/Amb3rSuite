# 14 — Kernel inventory and practical integration

The CSV ledger lists concrete headers from the inspected MuLIB tree and maps them to Amb3r subsystems. A header's presence is not a production feature claim or reviewed FFI approval. All paths are snapshot names: the separate upstream application-neutralization initiative may rename them; resolve by locked module identity, inspect current MANIFEST and regenerate adapters if source changes. Keep application-specific integration in Amb3r only.

## Actual circuit usage (reviewed upstream ABI)

See `examples/c/mulib_rc.c`, a schematic → deck → parse → OP → fixed BE → waveform chain. Under MuLIB include directory, compile with `cc -std=c11 -Wall -Wextra -Wpedantic -Werror -I "$MULIB/include" examples/c/mulib_rc.c -lm -o /tmp/amb3r_rc`. The example defines each needed implementation switch once. Actual APIs inspected:

- `mulib_ecad_schematic_add(&schematic, &component)` accepts flat R/C/I/V 2-terminal parts, up to 256; names at most 31 chars.
- `mulib_ecad_netlist_write(&schematic, deck, capacity, &used)` serializes the bounded deck.
- `mulib_spice_netlist_parse(deck, &net, &error_line)`; `mulib_spice_netlist_find_node(&net,"out")` ground 0, non-ground 1-based; max 128 nodes/1024 parts.
- `mulib_spice_op_solve(&net, volts, count)` dense linear OP R/I/V, capacitors open. Index voltages by `node-1`.
- `mulib_spice_tran_fixed(&net, dt, steps, probe, samples)` fixed BE, zero initial capacitor voltages, DC sources; no inductors. First sample at dt, not t=0.
- `mulib_wave_signal_push`, `mulib_wave_signal_interpolate`, `mulib_wave_signal_free`: zero-init owned series with analog kind; release once; borrowing samples invalidated by push/reallocation or free. RMS in this kernel measured over samples.

Separate TU pattern: one `mulib_impl.c` with all dependency macro definitions BEFORE headers, every other TU include declarations only. Derive implementation closure from actual MANIFEST and check static-inline vs externally linked. Test installed consumer and plugin collision. C11 + libm for these examples. `mulib-mune.h` needs parsec/jit/dynload plus its documented transitive macros; do not guess options or call upstream Lua API directly. Its known API includes `mulib_mune_create/destroy` (numeric environment) and `mulib_mune_state_create(options)` (full runtime), distinct objects. Implement real host callbacks from the pinned Mune manual and test execution/rejection in restricted mode.

## Adapter mapping and limitations

| Area | Foundation | Use and gap |
|---|---|---|
| DesignDB | eda-design-db/store/transaction/undo/ids | reuse algorithms via application-owned identity and revision adapter, bounded legacy models |
| ECAD | ecad-connect/schematic/netlist/erc | flatten design, translate persistent IDs to dense indices, initial 2-terminal profile |
| PCB | pcb-geometry/drc/router/stackup | integer-unit geometry and exact rules; bounded reference routes/formats |
| Numeric | num-csr/csc/sparse-lu/newton | canonical owned/view adapters, pivoted reference LU plus residual; symbolic/production performance outstanding |
| SPICE | spice-mna/device/diode/mosfet/tran | legacy vs newer representation mismatch, device derivative/checkpoint adapters; no full compact models |
| HWIL | hwil-module/context/verify | independent APIs; bounded graph width 64; application IR authoritative |
| Digital | dsim-logic4/scheduler/engine | scalar truth/resolution and event primitives; no full HDL scheduling conformance |
| Synthesis | synth-aig/bdd/cuts/cellmap | bounded Boolean operations; preserve sequential and X semantics |
| Formal | formal-cec/sat/bmc/pdr | CEC truth tables ≤6 inputs; reference explicit-state profiles vs symbolic algorithms; do not mislabel |
| Timing | timing-graph/sta/slack | scalar reference timing, real corner/arc providers needed |
| FPGA | fpga-rrgraph/pathfinder/bitstream | generic fabric, real vendor DB required |
| Media/waves | wave-store/decimate/fst | FST bounded encoding helpers not full file format; chunk/plot adapter |
| Field/RF | field-fem/fdtd/rf-touchstone | bounded 2D P1/1D reference where applicable; validated units and mesh |
| UI | immgtk/canvas/glx | select actual provider, separate draw state from design model |
| Extensions | mune/capbroker/ipc-framed | Mune subset and limits, trusted bootstrap isolation, host broker |
| AI | json/http/https/jsonrpc/sha | real TLS provider required, no raw secret exposure, bounded stream and schema |

## Foreign-language interoperability workflow

1. Pin header, dependency closure, target ABI, compiler flags and actual symbol linkage. Extract CDecl with Exotract. Raw static-inline bridging (`on1x/tools/on1x-exotract.py ... wrap-inline`) is bounded Linux x86-64, explicit symbols (up to 32), flat padding-free records/scalar pointers. Refer to current tool help; no automatic safe admission.
2. Define semantic ExoML contract: owned vs borrowed, capacities, alignment, initialization, aliasing, nullability, result validity, native destruction, errors, retention, callback/thread rules, effects, invalidation. Use ExoLib representation; review target-specific evidence. Do not invent grammar or sign a production approval with a disposable test key.
3. Generate external symbols and validate separate-TU linking, sizes, offsets, `_Generic` member checks where applicable. Review exact source+dependency hashes; invalidate on changes.
4. KernelBind admits only supported and reviewed schema. Current generic owner and pointer-heavy functions not automatically admitted; wrap a narrow scalar/flat-record facade in Amb3r, test under declared raw/trusted profile, label accurately. No direct resource call if unsupported.
5. On1x package offers typed application operations, safe lifetimes only if verified. Host owns resource handle registry; generation checks and scope binding; expose batch operations and explicit destruction. For future generalized language resource model, upgrade wrappers with move/borrow/drop and resource MIR.
6. Test negative paths, allocator faults, stale handles, cancellation, differential numerical results. Record ABI and semantic evidence separately. Do not add Amb3r-specific contracts to MuLIB.

## Build priorities

P0: one canonical DesignIR, linear RC C integration, source-map, project transaction, waveform plots, read-only plugin. P1: sparse solvers, model registry, generalized resource adapters, nonlinear simulation, HWIL RTL, digital event loop. P2: board routing, synthesis/formal, timing, mixed signal and AI integrations. P3: real production models, advanced physical flows, vendor devices and distributed jobs. No new kernel family until specific missing algorithm blocks a validated application slice.
