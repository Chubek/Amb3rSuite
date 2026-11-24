# Amb3r implementation handoff

Treat this workbook as a proposal and small executable reference suite, not an existing full application. Establish a separate Amb3r repository. Do not add Amb3r names, tests, docs, types, application contracts or project-specific logic to MuLIB. Keep generic upstream bug fixes independent. Pin current MuLIB and LibStone revisions and audit the actual current header APIs, especially after upstream name changes.

1. Read README and chapters 02–03, 10, 14–15. Run `python3 tests/check.py` and SDK CMake checks.
2. Begin M0/M1: define authoritative DesignIR, stable IDs, transaction validator and canonical RC circuit path. Reuse verified bounded MuLIB code through adapters; do not copy hundreds of headers.
3. Share ABI and IR schemas before parallel work. Use eight workstreams as specified in chapter 15, with a principal agent responsible for integration and real acceptance evidence.
4. Integrate actual C SDK, then Mune host callbacks and trusted restricted On1x bridge; admit foreign contracts only under independently reviewed policy. Generalized owner/borrow MIR/FFI is a prerequisite for richer native plugins. Keep speculative PPX syntax separate until admitted.
5. Design Elektra from reference subset; extend lexer/AST/type/lowering jointly with tests. Preserve legacy SPICE import as dialect profile.
6. Implement AI first as read-only tool broker, local-first policy, no raw shell or publish tool. Never send private designs or live credentials to a model without explicit permission.
7. Maintain actual capability matrix. Fail closed, output explicit unsupported, no fake kernels/providers, no silent simulator fallback. Keep test-only signing separate from production admission.
8. Deliver reproducible commands, tests run, failures/skips, exact supported profiles and remaining work. Do not claim the reference parser or SDK mock is a production implementation.
