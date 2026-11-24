# AMB3R — Engineering Workbook

**Architecture baseline 0.1 · 20 November 2026 · Independent repository**

An extensible electronics engineering environment: schematic and PCB design, circuit simulation, digital hardware compilation and optimization, verification, physical design, instrumentation and a programmable notebook. Elektra is its native engineering language. On1x is the intended application and extension language; C is the stable plugin ABI; Mune provides a Lua-language scripting environment. The AI assistant is a brokered engineering service, not an authority over designs.

## How to use this workbook

Start with the product scope and architecture; then implement the first vertical slice in the roadmap. All names, file formats, CLI commands and SDK interfaces defined here are **proposals for Amb3r**, not claims about existing application code. The actual MuLIB interfaces in the legacy RC example and kernel usage guide are pinned to a reviewed repository revision. Do not copy Amb3r-specific files into MuLIB. The separately versioned application should consume upstream generic kernels with adapters.

| Chapter | Contents |
|---|---|
| [01 Product](docs/01-product.md) | Workspaces, user workflows and scope |
| [02 Architecture](docs/02-architecture.md) | Repository, runtime, storage, build and process boundaries |
| [03 Design database](docs/03-design-db.md) | Identity, transactions, catalogue, IR lineage and formats |
| [04 ECAD and PCB](docs/04-ecad-pcb.md) | Schematic, connectivity, rules, layout and manufacturing |
| [05 Analog engine](docs/05-analog.md) | MNA/tableau, nonlinear integration, devices and analyses |
| [06 HWIL and HDL](docs/06-hwil.md) | Multi-level hardware IR, Verilog/VHDL/Vienna integration |
| [07 Simulation, synthesis and formal](docs/07-digital.md) | Event semantics, synthesis, proof and co-simulation |
| [08 Physical, RF and lab](docs/08-physical.md) | STA, FPGA, field solvers and instruments |
| [09 Elektra](docs/09-elektra.md) | Language design and semantics |
| [10 Extensibility](docs/10-extensibility.md) | C SDK, workers, Lua/Mune and On1x plugins |
| [11 PPX and On1x](docs/11-on1x-ppx.md) | Exclusive PPX catalogue, ABI and adoption plan |
| [12 AI engineering](docs/12-ai.md) | OpenAI, OpenCode, MCP, local models and validation |
| [13 UI and workflows](docs/13-ui.md) | Studio, notebook, canvas and CLI |
| [14 Kernel integration](docs/14-kernel-integration.md) | Actual APIs, mapping and admission workflow |
| [15 Quality and delivery](docs/15-roadmap.md) | Tests, eight workstreams, milestones and release gates |
| [16 References](docs/16-references.md) | Upstream pins, upstream docs and assumptions |

## Artifacts

- `diagrams/`: rendered SVGs and editable Graphviz sources, including a circuit diagram.
- `catalogues/`: kernel inventory, subsystem/feature mapping and extension-point catalogue.
- `schemas/`: draft JSON Schemas for projects, plugins, changesets and AI tool requests.
- `sdk/`: proposed C ABI header, executable reference host/plugin example and build file.
- `examples/`: SPICE decks, Elektra examples, Lua policy, actual-language On1x candidates, prospective On1x resource/PPX examples, and a MuLIB C circuit example.
- `tools/elektra_ref.py`: executable subset parser, unit checker and ideal DC resistor/voltage/current-source solver. It deliberately rejects the full-language features not implemented.
- `tests/`: independent reference checks and validation entry point.
- `AGENTS.md`: handoff to implementation agents. `VERIFICATION.md`: actual workbook verification, not upstream verification.

## Start locally

```sh
python3 tests/check.py
cmake -S sdk -B /tmp/amb3r-sdk-workbook
cmake --build /tmp/amb3r-sdk-workbook
ctest --test-dir /tmp/amb3r-sdk-workbook --output-on-failure
python3 tools/elektra_ref.py examples/elektra/divider.elek
```

The reference tools do not require network access or MuLIB. The MuLIB-dependent RC sample is separately built against the selected upstream snapshot. The workbook is a design pack plus small executable reference slices; it is not the Amb3r application, does not contain a completed production simulator, and does not confer foreign safety admission or claim compliance with EDA standards.
