# 08 — Physical design, RF, field and lab

## Timing and physical implementation

Build timing graph from mapped cells, pin timing arcs, clock definitions and parasitic networks. Early/late arrival, required times and slack by rise/fall and min/max corner; setup and hold signs differ. Handle clock uncertainty, generated clocks, false paths, multicycle paths and asynchronous groups explicitly. Combinational cycles report error; disabled arcs and exceptions are provenance-tagged. Initial STA is single corner acyclic graph with scalar delays; Liberty parser/table interpolation, SDC and SPEF profiles must be explicit. Compare critical paths to OpenSTA for supported subsets.

ASIC: floorplan, ports/macros, placement (analytic or annealing), legalization, congestion/global route, detailed route, RC extraction, timing closure, sign-off export only with provider evidence. LEF/DEF and physical formats require full format support or external interoperable provider. PDK access is user-authorized, licence-aware and never silently uploaded.

FPGA: architecture catalogue → pack logic → place clusters → build routing resource graph → negotiated congestion/Pathfinder → timing → emit validated target-specific representation. Generic bit packing and FASM helper are not proof of bitstream compatibility. Start with abstract educational fabric, then a device family using licensed real architecture data and independent tools such as VTR/nextpnr where supported.

## RF and electromagnetic simulation

Touchstone parsing, reference impedance, frequency unit, S/Z/Y conversion, cascades (ABCD for two-ports), matching, Smith chart, microstrip approximations, transmission line response and tolerance. Report frequency range, reference impedance and approximation assumptions. A common 50 Ω reference is not universal. Field solver pipeline mesh → material tensors → boundary conditions → assemble discretization → solve → convergence/refinement → post-process. Start with electrostatic 2D FEM and Poisson reference; finite difference/FDTD for bounded profiles, stability/CFL and PML provider validation. Thermal/electrothermal iterate loss and temperature with explicit convergence criteria. Verify against analytical capacitor/field cases and grid refinement. Do not claim 3D EM or manufacturing signoff from scalar kernels.

## Instrumentation and notebook lab

SCPI transport is explicit capability. Device catalogue contains identity, address, allowed commands, limits and calibration. Use mock instrument by default; live hardware must be separately authorized. Read-only query vs output-setting commands are distinct capabilities. Enforce user-configured current/voltage/power limits and interlocks outside LLM control. No agent can turn on a supply, switch a relay or emit arbitrary SCPI. Deadline, cancellation and disconnect recovery are mandatory; never promise physical safe state solely from software. Capture measurement uncertainty, timestamp, units, instrument version and calibration. Compare simulated and measured signals with alignment/uncertainty, not silent resampling.
