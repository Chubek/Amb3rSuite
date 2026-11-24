# Structural draft schemas

Version 1 proposal; not an implemented persistent format. Structural validation is necessary but not sufficient. Enforce per-kind known fields, ID/revision relationships, create/update/delete preconditions, finite JSON, grants, size/depth, unit/semantic checks and publication atomically in host code. Reject duplicate JSON keys and limit input before parsing; the generic argument/value object in these schemas needs per-tool or per-kind validation. A manifest is inert and never grants capabilities. The AI tool list omits direct apply.
