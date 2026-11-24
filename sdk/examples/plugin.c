#include "amb3r_sdk.h"
#include <stdio.h>
#define S(s) ((amb3r_span){s,sizeof(s)-1u})
static amb3r_status inspect(const amb3r_host_v1 *h, amb3r_snapshot revision, void *unused) {
    (void)unused;
    uint64_t count=0;
    amb3r_status s=h->object_count(h->context,revision,S("component"),&count);
    if (s!=AMB3R_OK) return s;
    char msg[80];
    int n=snprintf(msg,sizeof msg,"design contains %llu components",(unsigned long long)count);
    if(n<0 || (size_t)n>=sizeof msg) return AMB3R_LIMIT;
    return h->emit_diagnostic(h->context,revision,S("EXAMPLE.COUNT"),(amb3r_span){msg,(size_t)n});
}
static amb3r_status init(const amb3r_host_v1 *h) {
    if (!h || h->abi_version!=AMB3R_ABI_V1 || h->struct_size<sizeof *h) return AMB3R_ABI;
    return h->register_command(h->context,S("example.count"),inspect,NULL);
}
static void shutdown_plugin(void) {}
const amb3r_plugin_v1 *amb3r_plugin_entry_v1(void) {
    static const amb3r_plugin_v1 p={AMB3R_ABI_V1,sizeof p,{"example",7},
        AMB3R_CAP_READ|AMB3R_CAP_DIAGNOSTIC|AMB3R_CAP_REGISTER,init,shutdown_plugin};
    return &p;
}
