# Example index and execution status

| Source | Status | Use |
|---|---|---|
| `elektra/divider.elek` | Executed in included Python reference parser | Linear circuit with dimension-checked primitives |
| `elektra/*.elek.txt` | Proposed full language | Experiments, hardware, boards, parametric components, model equations |
| `c/mulib_rc.c`, `c/logic4.c` | Adapted from inspected native interfaces; not built here | Build against pinned MuLIB; verify after upstream migration |
| `on1x/*.on1x` | Candidate using documented existing language features; not built here | Compiler and policy examples |
| `on1x/*.on1x.txt` | Illustrative future syntax and APIs | Generalized resources and exclusive PPXs |
| `lua/erc_rule.lua` | Proposed application adapter; not executed | Mune script extension design |
| `spice/rc.cir` | Standard-style SPICE deck, not executed here | Optional independent simulator with matched initial conditions |
| `spice/rc-legacy.deck` | Bounded numeric-value parser profile | Actual legacy MuLIB syntax |
| `hdl/counter.v`, `hdl/counter.vhd` | Reference source, not compiled here | Digital reset/enable semantics |
| `hwil/*.txt` | Proposed language/IR examples | HWIL and Vienna |
| `ai/*.json` | Inert fixtures, no network call | API message envelopes |
| `ai/broker_mock.py` | Executed local policy reference | Scoped revision reads and inert proposals |

Fixture project and plugin manifests use illustrative hashes, not installed artifacts, actual signature or grants. All source examples are original workbook material, not extracted application source. The separate `sdk/` C examples build without upstream dependencies.
