# 01 — Product charter

Amb3r unifies three original workspaces: **Electronics CAD**, **Electronics Design Automation** and **SPICE simulation**. Extend them with a digital hardware workbench and a notebook/lab environment. Do not build five disconnected products: each workspace reads a revision of one design model, and all write actions enter one validated transaction system.

## Product surfaces

| Surface | Responsibilities | First vertical slice |
|---|---|---|
| Studio / CAD | symbol editor, hierarchical schematics, footprint library, PCB, cross-probing, differential review | edit an RC schematic, select a node and plot it |
| Automation / EDA | ERC/DRC, constraints, BOM, variants, rule packs, design rewrites, placement/routing | run ERC, show rule evidence, preview a fix |
| Analog Lab | OP, DC, AC, transient, sweeps, measurement, sensitivity, tolerance, noise | RC OP/transient with numerical oracle |
| Digital Lab | Elektra/HDL source, HWIL viewer, simulator, synthesis, equivalence, timing | counter testbench, AIG pass and equivalence |
| Physical Lab | PCB/ASIC/FPGA flows, timing closure, extraction, thermal and RF | board DRC and simple impedance estimate |
| Notebook | Elektra/On1x/Lua/Markdown cells, datasets, reproducible experiments, result provenance | run a parameter sweep and render plot/table |
| Console / CLI | headless compile, simulate, verify, inspect, export and reproduce | CI script drives same engine as UI |
| Copilot | evidence-grounded design Q&A, constrained proposals and analysis | explain an ERC warning with cited design IDs |

The first target is Linux desktop/headless with deterministic builds. Cross-platform rendering and provider support follow after the core works. Keep formal hardware and PCB manufacturing verification explicit. A generated report never certifies electrical safety, manufacturability or regulatory compliance by itself.

## Core principles

- Stable identity, revision-local indices. Never make visual coordinates the sole netlist identity.
- Separate immutable logical design snapshots from mutable UI selections and ephemeral solver state.
- Explicit units, dimensions, clock domains, logic X/Z and numerical tolerances.
- One authoritative rule/transaction/verification path for UI, CLI, scripts and plugins.
- Export/import/simulation results contain source revision, catalogue locks, tool versions, selected profiles and warnings.
- Fail closed for unsupported features, untrusted plugins, failed convergence and stale edits.
- Own only Amb3r-specific implementations in Amb3r; depend on MuLIB and LibStone through versioned public interfaces.

## Users and workflows

A student can draw a circuit, derive transfer functions, simulate and write a notebook. A hardware engineer can review pin and net constraints, board clearances, simulation and part revisions. A language/EDA developer can write Elektra generators, C device providers, Mune scripts and On1x PPXs. A verification engineer can inspect HWIL, testbench evidence, timing paths and counterexamples. A production flow can export deterministic artifacts subject to explicit human sign-off.

## Boundaries

Do not try to replace all of KiCad, ngspice, Yosys, commercial layout tools or SPICE model compilers in release 0.1. Reference providers serve as differential oracles or explicit optional backends. The custom engine and design database remain authoritative. Full SystemVerilog, VHDL, vendor FPGA bitstreams, production compact models and advanced RF/field simulation are multi-release efforts. Feature support is an executable capability matrix, not marketing.
