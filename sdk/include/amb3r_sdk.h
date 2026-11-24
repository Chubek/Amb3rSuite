#ifndef AMB3R_SDK_H
#define AMB3R_SDK_H
/* Proposed ABI v1, executable reference subset. No binary stability promise yet.
 * All strings passed by pointer+length are borrowed for the duration of the call.
 * All callbacks are synchronous, thread-confined and must not throw across C. */
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
#define AMB3R_ABI_V1 UINT32_C(1)
typedef uint32_t amb3r_status;
enum { AMB3R_OK=0, AMB3R_INVALID=1, AMB3R_ABI=2, AMB3R_DENIED=3,
       AMB3R_STALE=4, AMB3R_LIMIT=5, AMB3R_DUPLICATE=6, AMB3R_FAILED=7,
       AMB3R_UNSUPPORTED=8 };
typedef uint64_t amb3r_snapshot; /* Host-issued revision token; no raw pointer. */
typedef struct { const char *data; size_t size; } amb3r_span;
#define AMB3R_CAP_READ UINT64_C(1)
#define AMB3R_CAP_DIAGNOSTIC UINT64_C(2)
#define AMB3R_CAP_REGISTER UINT64_C(4)
typedef struct amb3r_host_v1 amb3r_host_v1;
typedef amb3r_status (*amb3r_command_fn)(const amb3r_host_v1 *, amb3r_snapshot, void *);
struct amb3r_host_v1 {
    uint32_t abi_version, struct_size;
    void *context;
    uint64_t granted;
    /* Register only during initialization; host copies key, not context. */
    amb3r_status (*register_command)(void *, amb3r_span, amb3r_command_fn, void *);
    /* The reference model only supports the count of a typed object kind. */
    amb3r_status (*object_count)(void *, amb3r_snapshot, amb3r_span, uint64_t *);
    /* Copied into a bounded staging sink; published only if command succeeds. */
    amb3r_status (*emit_diagnostic)(void *, amb3r_snapshot, amb3r_span, amb3r_span);
};
typedef struct {
    uint32_t abi_version, struct_size;
    amb3r_span plugin_id;
    uint64_t required_capabilities;
    amb3r_status (*init)(const amb3r_host_v1 *);
    void (*shutdown)(void); /* Called after successful init, once. */
} amb3r_plugin_v1;
/* Provider exports this entry; no code lookup is performed by reference host. */
const amb3r_plugin_v1 *amb3r_plugin_entry_v1(void);
#ifdef __cplusplus
}
#endif
#endif
