# 07 — Digital simulation, synthesis and formal verification

## Simulation kernel

Use event key `(time_ticks, delta, region, sequence)`, checked integer timebase. A canonical scheduler has deterministic ordering; a frontend-specific region map models VHDL delta updates or Verilog active/inactive/NBA/monitor phases for admitted subsets. Events contain stable driver/signal identity, value, delay semantics and cancellation token. Update driver values, resolve, awaken sensitive processes, schedule assignments and repeat until quiescent. Impose delta and event budgets; report oscillation with a trace. No zero-delay scheduler can silently spin forever.

Four-state bitvectors retain known and high-impedance masks. For width expansion distinguish zero/sign extension and X extension. Resolution: no drivers Z; opposing known driven values X; strengths only if explicitly supported. Blocking versus nonblocking assignments require separate event semantics; transport and inertial delays differ, including cancellation of pending inertial pulses. Testbench supports clock/reset, deterministic stimuli, assertions, coverage and expected traces. Probe and time scale metadata are mandatory.

## Mixed signal

Analog time is continuous, digital time discrete. Define A/D threshold and hysteresis, D/A output levels and finite rise/fall impedance. Synchronize by global event horizon; analog step cannot overrun a known digital event; detect analog threshold crossings via root localization, rollback to crossing, schedule digital event and restabilize. Co-simulation coordinator checkpoints both engines before speculative advances. Choose tolerances and min delay; report oscillatory feedback and incomplete convergence. Unknown logic must map only through explicit model policy; no arbitrary 0 substitution.

## Synthesis pipeline

Elaborated RTL → canonicalization → width/legalization → constant folding → dead code elimination → FSM extraction/encoding → arithmetic and memory inference → bit lowering → AIG/XAG/MIG optimization → cut enumeration → NPN normalization → cell/LUT mapping → timing-aware rewrite → verification. Optimize area/delay/power with explicit cost units, constraints and ties. E-graph saturation budget and extraction cost, BDD variable order, bounded truth tables and SAT checks each have different capacity profiles. Retiming requires legal clock/reset domains and equivalent sequential behavior; a retiming label checker is not a retiming optimizer. Preserve black-box assumptions.

## Formal

- Combinational equivalence: shared input mapping, miter, SAT UNSAT means equivalent under assumptions; SAT returns witness, UNKNOWN not proof. Truth tables are exact only in bounded width.
- Sequential equivalence: state relation, reset/initial-state assumptions, time mapping, induction or bounded counterexample. State-mapping assumptions must be explicit.
- BMC: transition relation unrolled to bound k; no counterexample within k is not unbounded proof. k-induction needs base and induction. PDR/IC3 must be genuine symbolic blocking or labelled explicit state reference only.
- Properties: safety, eventually under fairness for liveness, clocked assertions, CDC/RDC heuristics and synchronizer policies. Distinguish proof, counterexample, timeout, unsupported and inconclusive. Record solver version, proof artifacts if available and source traces.

## Testbench example

8-bit counter increments on rising edge; synchronous active-high reset overrides enable; expected 0,1,2, hold,0. Compare engine traces to an independent event oracle and a pinned Verilog simulator if installed. For synthesis compare truth table or SAT witness pre/post for small circuits, then sequential equivalence under explicit reset. Use randomized differential tests with seed capture, X/Z cases and invalid design rejection.
