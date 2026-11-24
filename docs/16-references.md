# 16 — References and provenance

## Repository snapshot

- MuLIB: https://github.com/Chubek/mulib, inspected HEAD `8a2c380e2866835e0812178c94b8689d317a9219` (2026-11-20 09:29:39 UTC), include tree `b0f5816a0f598c6519abbf883179c86841b0b6d8`.
- Consolidation source revision `e93ea4855828d62d89154a66b4b24593819d37cf`: https://github.com/Chubek/mulib/tree/e93ea4855828d62d89154a66b4b24593819d37cf/consolidation . Historical verification only, not a workbook test run. Upstream neutralization may change the names used in this workbook.
- LibStone: https://github.com/Chubek/libstone . Prior consolidation pinned `3399047f6c6328b8f07788795c610699e66c060a`; the later sync may change the pin. Resolve actual gitlink before building. No direct claim that every LibStone feature is implemented or usable.
- Selected source inspection: `include/mulib-{ecad-schematic,spice-netlist,spice-op,spice-tran,spice-mna,wave-signal,hwil-context,dsim-logic4,formal-cec,mune,num-csr}.h` and consolidation C reference workflow. See pinned repository paths. The workbook example is an independently adapted version of the workflow, not a complete upstream kernel distribution.

## AI interface references (consulted 2026-11-20)

- OpenAI Responses API: https://developers.openai.com/api/reference/resources/responses/methods/create
- OpenAI function calling: https://developers.openai.com/api/docs/guides/function-calling
- OpenCode HTTP API (experimental): https://opencode.ai/docs/api
- OpenCode SDK: https://opencode.ai/docs/build/sdk/
- OpenCode network client: https://opencode.ai/docs/build/client
- MCP specification and revision news: https://modelcontextprotocol.io/ and https://blog.modelcontextprotocol.io/posts/2026-07-28/
- Ollama OpenAI compatibility: https://docs.ollama.com/api/openai-compatibility

The design uses general protocol patterns and does not freeze external model IDs or promise exact version-specific server compatibility. Test the installed provider against its documented schema. No API calls, live credentials or network agent execution were tested.

## Technical reading and potential test providers

- Ho, Ruehli, Brennan, “The Modified Nodal Approach to Network Analysis” (1975): foundational MNA.
- Nagel, SPICE2 (1975); Kundert, The Designer's Guide to SPICE and Spectre: numerical circuit simulation.
- ngspice: https://ngspice.sourceforge.io/ ; Xyce: https://xyce.sandia.gov/ ; SuiteSparse: https://github.com/DrTimothyAldenDavis/SuiteSparse . Optional solver/oracle references, not bundled.
- SUNDIALS: https://computing.llnl.gov/projects/sundials ; OpenVAF: https://openvaf.semimod.de/ . DAE/model provider candidates.
- IEEE 1364/1800, IEEE 1076: language standards for Verilog/SystemVerilog/VHDL; use licensed applicable version and declare subset.
- Yosys: https://yosyshq.net/yosys/ ; ABC: https://people.eecs.berkeley.edu/~alanmi/abc/ ; Icarus: https://steveicarus.github.io/iverilog/ ; Verilator: https://verilator.org/ ; GHDL: https://ghdl.github.io/ghdl/ . Reference tooling.
- OpenSTA: https://github.com/The-OpenROAD-Project/OpenSTA ; OpenROAD: https://theopenroadproject.org/ ; VTR: https://verilogtorouting.org/ ; nextpnr: https://github.com/YosysHQ/nextpnr . Physical design references.
- KiCad: https://www.kicad.org/ ; Gerber format: https://www.ucamco.com/en/gerber ; Touchstone: https://ibis.org/touchstone_ver2.0/ . Exchange specifications; formal compliance not established.

External links other than inspected repository and AI protocol documentation are suggested reading, not independently audited latest compatibility or licence claims. No external third-party code or model weights are bundled.
