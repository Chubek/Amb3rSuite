# 15 — Implementation workbook and acceptance gates

## Eight workstreams

| Agent | Scope | Relative emphasis | Dependencies |
|---|---|---:|---|
| 1 | DesignIR, catalogue, transactions, storage and adapters | 18% | Shared ABI first |
| 2 | ECAD, PCB, geometry, Studio canvas | 13% | 1 |
| 3 | Analog CircuitIR, SPICE, numerical solvers, waveforms | 18% | 1 |
| 4 | Elektra frontend, HWIL, HDL, digital event engine | 16% | 1, shared grammar |
| 5 | Synthesis, formal, timing, physical/FPGA/RF profiles | 10% | 3/4 |
| 6 | C SDK, Mune/On1x plugins, PPX and ABI admission | 13% | 1, 3/4 contracts |
| 7 | AI gateway, notebook, CLI and UI service integration | 6% | 1, 6 |
| 8 | Independent QA, differential and application workflows | 6% | starts immediately |

Principal agent coordinates shared schemas, exclusive file ownership and integration. Do not run eight conflicting implementations of the design DB or type system. Freeze versioned interface proposals before parallel work; merge in dependency order. Use worktrees where possible, no unrelated edits. Treat emphasis allocation as guidance. Build functional vertical slices, not declarations. Preserve upstream purity.

## Milestones

| Gate | Exit evidence |
|---|---|
| M0 skeleton | pinned MuLIB/LibStone, clean native build, schema and ABI contracts, no hidden network requirements |
| M1 RC vertical slice | Elektra and schematic produce same CircuitIR, OP + BE oracle, waveform display, project roundtrip, immutable jobs; duplicate IDs/stale edits reject |
| M2 application integration | generic C plugin read-only command, Mune bounded rule, authorized On1x plugin/bridge, candidate changeset and undo, consistent capability matrix |
| M3 practical analog | sparse linear assembly, diode Newton, adaptive time and step rollback, AC, sweeps, independently checked derivatives and failures |
| M4 digital compiler | Elektra and bounded Verilog source to verified HWIL, counter, deterministic events, equivalence and VCD |
| M5 board flow | footprints, netlist sync, placement, routing/DRC, reviewed exchange output with independent parser |
| M6 extensible engineering | typed resource bindings where admitted, PPX suite subsets, notebook, AI read-only grounding and candidate review, reproducibility manifests |
| M7 advanced providers | sparse performance, mixed signal, timing, physical, FPGA target DB, RF and field verified profiles |

Acceptance is by subset, not milestone names. A feature is EXECUTABLE, PARTIAL, DISCOVERY_ONLY, PROVIDER_REQUIRED or UNSUPPORTED; distinguish native C availability from On1x admission. Never count registered names as implementations. Maintain issue list with dependencies, exact reproducible commands, tests and evidence.

## Tests and oracles

- Unit: parsing, dimensions, IDs, generation handles, conversions, stamp signs, scheduler order, bit-width, plugin ABI record bounds.
- Property: connectivity under edit order, deterministic serialization, sparse matrix residuals, translation validation, candidate failure atomicity, no ghost events.
- Integration: UI/CLI same commands, circuit to waveform, subcircuit flatten, board net mapping, plugin denial, notebook replay, stale AI proposal.
- Differential: ngspice/Xyce with matched init/model/options; Icarus/Verilator/GHDL for supported HDL; Yosys/ABC/SAT solvers for Boolean logic; OpenSTA for timing; KiCad parser for exchange; VTR/nextpnr for supported fabric. Missing oracle is SKIP not PASS. Compare dimensions, tolerance, numerical values, indicated state/event semantics, not only text.
- Fuzz: Elektra, SPICE, HDL, binary/project import, provider manifest, IPC, waveform; finite length/depth and time budgets. Invalid inputs must not partially publish.
- Security: capability denial, malicious package, stale handles, shared-memory mutation, unsafe native constructor, credential redaction, prompt injection and budget enforcement. TSan for actual parallel code and ASan/UBSan/LSan for native ownership.
- Performance: sparse fill, matrix size/time/peak memory, Newton iterations, accepted/rejected steps, events/sec, waveform throughput, UI latency, plugin transport overhead; benchmark fixtures with revision and machine profile, no unsupported claims.

## Workbook exercises

1. Add an RC analysis to the C example, sweep R2 and compare DC and BE reference. Record tolerances and failures.
2. Extend Elektra parser to accept pure parameters and dimensions before adding transistor models. Write malformed-unit and singular cases.
3. Implement a read-only ERC C plugin using the reference SDK pattern. Try duplicate IDs and missing grant; verify denied calls.
4. Create Mune rule pack that reports unconnected power pins; build authoritative host callback first. Prevent untrusted script access to OS.
5. Implement a bounded `Units` PPX using canonical On1x transport; reject unsupported new syntax explicitly.
6. Add digital counter, verify reset/enable traces and compare synthesis with original behavior.
7. Expose AI diagnosis on immutable revision, test false citation and stale proposal; prove no direct publication.
8. Port RC workflow to On1x only after reviewed resource/aggregate contracts. Track which operations still need native glue.

## Release and governance

Keep a human sign-off for design/fabrication and physical instrument actions. Reproducible offline build, licence inventory, signed package metadata, vulnerability reporting, ABI migration notes, source hash invalidation, supported platform matrix. User remains owner of final design decisions. No cross-project names or fixtures upstream. A release includes actual executed tests, skipped cases, performance data, unimplemented features and clear versioned format profile.
