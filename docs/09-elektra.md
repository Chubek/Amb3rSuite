# 09 — Elektra: an electronics engineering language

## Design

Elektra is Amb3r's native, declarative-first, typed engineering DSL. It is not another general-purpose programming language or a SPICE syntax alias. It describes circuits, netlists, hardware modules, testbenches, measurements, constraints, component libraries, board intents, solver experiments and project generators. Pure compile-time functions and finite elaboration allow parameterized hardware. Commands that actually execute jobs or modify the design are host-authorized operations outside pure elaboration.

| Domain | Elektra construct | Lowering target |
|---|---|---|
| Analog | circuit, component, model, connect, equation | CircuitIR / model stamp interface |
| Digital | module, signal, reg, assign, on | HWIL H1/H2 |
| Libraries | symbol, footprint, component, param | catalogue records |
| PCB | board, place, route, constraint | DesignIR candidate |
| Experiments | experiment, analysis, probe, measure, sweep | job recipe |
| Verification | assert, property, testbench | test properties / HWIL |
| Interchange | import spice, import verilog, export | explicit provider request |

## Concrete syntax proposal v0.1

```elektra
package lab.divider;
circuit Divider {
  net vin, out, gnd;
  ground gnd;
  V1: Voltage(vin, gnd, 8 V);
  R1: Resistor(vin, out, 1 kohm);
  R2: Resistor(out, gnd, 3 kohm);
  C1: Capacitor(out, gnd, 1 uF);
}
experiment Charge for Divider {
  op;
  tran step 75 us stop 6 ms initial zero;
  probe V(out);
  measure settled = V(out) at 6 ms;
  assert settled > 5.9 V;
}
```

Full examples under `examples/elektra/`. The executable reference subset accepts only the divider form without package, capacitor or experiment. Its strict grammar is below; the larger syntax is a specification, not compiled code. SPICE remains an import/export format with dialect profiles. Never infer Elektra meaning from SPICE suffix case: `M` in many SPICE dialects means milli, while Elektra requires an explicit SI unit symbol.

## Lexing and grammar

UTF-8 source, ASCII identifiers in first release; reserve keywords; strings with explicit escapes; `//` and `/* */` comments in full grammar (reference subset only `//`). Case-sensitive identifiers. Quantity syntax is number plus unit token (spaces required in reference parser). Full grammar sketch:

```ebnf
file        = [ "package" qualified ";" ] { import | declaration } ;
import      = "import" (qualified | dialect string) [ "as" ident ] ";" ;
declaration = circuit | component | module | board | experiment | testbench | model | function ;
circuit     = "circuit" ident [ parameters ] "{" { net | ground | instance | generate | connect } "}" ;
net         = "net" ident { "," ident } ";" ;
ground      = "ground" ident ";" ;
instance    = ident ":" qualified "(" [ expr { "," expr } ] ")" ";" ;
experiment  = "experiment" ident "for" qualified "{" { analysis | probe | measure | assertion | sweep } "}" ;
analysis    = "op" ";" | "tran" "step" expr "stop" expr "initial" ("zero" | "op") ";"
            | "ac" "decade" integer "from" expr "to" expr ";" ;
module      = "module" ident "(" [ port { "," port } ] ")" "{" { signal | register | assignment | process } "}" ;
port        = [ "in" | "out" | "inout" ] ident ":" type ;
expr        = Pratt expression with calls, arithmetic, comparisons and unit literals ;
```

Operator precedence: postfix/call, unary, multiplicative, additive, comparison, equality, boolean AND/OR. No implicit dimension-changing casts. Pure expressions have finite evaluation budgets; recursion disallowed initially, bounded `generate for` expands finite compile-time ranges. Parameter dependency cycles reject. Packages use pinned catalogue imports and source provenance. Separate namespace for net, instance, parameter, type and package; ambiguous references reject. Unknown attributes are preserved only in explicit metadata blocks, never treated as semantic no-ops.

## Type system and dimensions

SI dimension vector `(kg,m,s,A,K,mol,cd)`; V=(1,2,-3,-1,0,0,0), Ohm=(1,2,-3,-2,0,0,0), F=(-1,-2,4,2,0,0,0). Numeric quantities combine exponent vectors by multiplication/division; addition, comparisons and assignment require identical dimensions. Kelvin absolute temperature versus temperature difference explicitly distinct; Celsius projection is affine. Frequency vs angle-rate distinguish tagged semantics. Hardware types `bits<N>`, `logic<N>`, `clock`, `reset`, `analog<voltage>`, port direction and discipline. No implicit numeric conversion between analog and digital. Casts and mixed signal bridges explicit. Width overflow policy `wrap`, `saturate` or `checked` by operation/profile.

## Compiler pipeline

Lexer → AST with source maps → package/catalogue resolution → constraint/type checking → pure elaboration → candidate DesignIR/CircuitIR/HWIL/JobIR → authoritative validator → publication. Separate language server diagnostics and formatter from execution. Elektra parser can be implemented in On1x using Firestone-backed grammar facilities once supported; C/C++ reference frontend may initially serve the same AST contract. PPX Elektra embeds source and calls this same frontend, never generates unchecked trusted IR.

## Reference subset (implemented in tools/elektra_ref.py)

```ebnf
file = "circuit" IDENT "{" "net" IDENT { "," IDENT } ";"
       "ground" IDENT ";" { IDENT ":" KIND "(" IDENT "," IDENT "," NUMBER UNIT ")" ";" } "}" EOF ;
KIND = "Resistor" | "Voltage" | "Current" ;
```

Bounded file, identifier and matrix size; comments `//`; positive resistances; finite values; declared distinct terminals; exactly one ground; unique signal and component names. Only DC ideal linear elements. Outputs JSON node voltages and source currents, solves pivoted dense MNA and checks scaled residual. Singular networks reject. It does not execute arbitrary code, import files, generate hardware or perform transient simulation. This is an executable language-design reference, not the complete compiler.

## Advanced language ideas

First-class parametric cells, finite structural generators, typed model equations with AD, generative footprint DSL, constraints with named assumptions, design variants, pattern-driven EDA transformations, units-aware assertions, reusable analysis recipes, waveform algebra, notebook cells, formal temporal properties and target descriptions. Implement one feature at a time with grammar, semantics, diagnostics, lowering and executable tests. Avoid a Turing-complete compile-time DSL until determinism, capability and resource constraints are established.
