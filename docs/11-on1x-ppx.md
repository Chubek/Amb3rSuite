# 11 — On1x library architecture and exclusive PPXs

The application owns `on1x/ppx/` and `on1x/library/` in its own repository. All Amb3r-specific packages and macro languages stay here. Generic upstream PPX facilities may be improved independently without depending on Amb3r.

## Proposed PPX suite

| PPX | Intent | Typed expansion / evidence |
|---|---|---|
| Elektra | embedded Elektra source | versioned source asset and checked frontend call |
| SPICE | embedded SPICE deck | dialect-tagged source buffer and import call |
| Circuit | structural circuit literal | DesignIR candidate builder calls |
| Netlist | explicit nodes/devices | checked typed circuit values |
| Units | dimensional numeric syntax | dimension-tagged values and checked conversions |
| Hardware | RTL descriptions | HWIL candidate builder |
| Verilog / VHDL | language embeds | source asset + frontend request |
| Vienna | architecture descriptions | target catalogue candidate |
| BitVector | width-checked hardware ops | typed bitvector library calls |
| RegisterMap | register fields/access policies | data map, C/HDL/driver generators |
| Timing | clock and timing constraints | versioned constraint records |
| Assertions | properties and assumptions | formal property candidate |
| StateMachine | Mealy/Moore machines | explicit state and transition IR |
| AnalogModel | equations and disciplines | model evaluator/derivative expression IR |
| AutoDiff | derivative requests | typed expression graph and verified derivative |
| Symbol / Footprint | library CAD definitions | candidate catalogue geometry, pin mapping |
| DesignRules | rule and exception DSL | validated rule facts |
| Catalogue | provider descriptions and requirements | inert metadata only |
| Testbench | timed stimuli, expectations | bounded simulation recipe |
| Waveform | probe algebra and reductions | typed measurement recipe |
| Sweep | parametric experiments | deterministic job graph |
| RegisterTransfer | clocked RTL assignments | validated combinational/sequential regions |
| Synthesis | pass pipelines | explicitly selected pass IDs and constraints |
| Layout | floorplan and routing intent | board/physical candidate constraints |

An extension transforms source/AST candidates into ordinary typed On1x code, a checked asset or a request to the canonical Elektra/HWIL compiler. It must not bypass semantic checking, register trusted contracts, run hardware or silently perform external I/O. Hygienic bindings, deterministic output, bounded expansion and source mapping mandatory. PPX-v1 currently has a restricted schema; new constructs not transported must be rejected or encoded as existing supported carrier data with ordinary readmission. Full PPX-v2 and new grammar constructs are upstream prerequisites, not assumptions.

## Example future surface

```on1x
# PROPOSED, not current On1x syntax or PPX transport.
@enable Amb3r.Units;
@enable Amb3r.Elektra;
# Actual carrier syntax must follow the admitted PPX interface.
# Elektra embed compiles a source asset, never injects a trusted handle.
```

See `examples/on1x/ppx-concepts.on1x.txt` and `examples/on1x/resource-workflow.on1x.txt` for illustrative extended syntax. `examples/on1x/ref-exchange.on1x` uses documented existing features and is a candidate for the pinned compiler. No On1x compiler build has been executed for this workbook.

## Library surface

`amb3r.design`, `.ecad`, `.pcb`, `.circuit`, `.spice`, `.hwil`, `.verilog`, `.vhdl`, `.vienna`, `.dsim`, `.synthesis`, `.formal`, `.timing`, `.fpga`, `.wave`, `.rf`, `.instrument`, `.sdk`, `.notebook`, `.ai`. Keep typed resource wrappers, explicit effectful commands and pure computation separate. The C host can own complex native state until general On1x resources exist, but label scalar host bridge as transitional, not safe general FFI. Prefer high-level batch calls over one native call per pixel, stamp or event.

## Current-stage adoption

At the reviewed upstream revision, `borrow` / `ref` support named places, `ref_replace` exchanges owned/managed values, finite `own<Named>` has restricted direct-C11 cleanup; broad resource containers, aggregate FFI, field/index loans and resource MIR remain limited. Typed cooperative channels support bounded pointer-free payloads only. Raw static-inline wrappers provide external symbols but no semantic admission. Use a small reviewed scalar/flat-record interface first; later migrate to owning handles, buffers, generic vectors and checked aggregate bindings. Do not use integer handles as safe language owners without validation and lifecycle enforcement. On1xRT dynamic loading is trusted native Linux/glibc, not an isolated plugin profile. MIR verification is structural, not automatically equivalence.
