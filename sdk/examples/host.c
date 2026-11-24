/* In-process TRUSTED reference host. Not a loader, sandbox, or full registry. */
#include "amb3r_sdk.h"
#include <stdio.h>
#include <string.h>
#define S(s) ((amb3r_span){s,sizeof(s)-1u})
typedef struct {
    uint64_t caps, revision, components;
    int registering, running, failed;
    amb3r_command_fn command; void *userdata;
    char name[64], code[64], message[128];
} context;
static int equal(amb3r_span a, const char *b) {
    return a.data && a.size==strlen(b) && !memcmp(a.data,b,a.size);
}
static int copy(char *out,size_t n,amb3r_span s) {
    if(!s.data || !s.size || s.size>=n || memchr(s.data,0,s.size)) return 0;
    for(size_t i=0;i<s.size;++i) if((unsigned char)s.data[i]<32 || (unsigned char)s.data[i]>126) return 0;
    memcpy(out,s.data,s.size);out[s.size]=0;return 1;
}
static amb3r_status reg(void *v,amb3r_span name,amb3r_command_fn fn,void *u) {
    context *c=v;
    if(!c->registering || !(c->caps&AMB3R_CAP_REGISTER)) {c->failed=1;return AMB3R_DENIED;}
    if(c->command) {c->failed=1;return AMB3R_DUPLICATE;}
    if(!fn || !copy(c->name,sizeof c->name,name)) {c->failed=1;return AMB3R_INVALID;}
    c->command=fn;c->userdata=u;return AMB3R_OK;
}
static amb3r_status count(void *v,amb3r_snapshot r,amb3r_span kind,uint64_t *out) {
    context *c=v;
    if(!c->running || !(c->caps&AMB3R_CAP_READ)) {c->failed=1;return AMB3R_DENIED;}
    if(r!=c->revision) {c->failed=1;return AMB3R_STALE;}
    if(!out || !equal(kind,"component")) {c->failed=1;return AMB3R_INVALID;}
    *out=c->components;return AMB3R_OK;
}
static amb3r_status emit(void *v,amb3r_snapshot r,amb3r_span code,amb3r_span message) {
    context *c=v;
    if(!c->running || !(c->caps&AMB3R_CAP_DIAGNOSTIC)) {c->failed=1;return AMB3R_DENIED;}
    if(r!=c->revision) {c->failed=1;return AMB3R_STALE;}
    if(c->code[0] || !copy(c->code,sizeof c->code,code) || !copy(c->message,sizeof c->message,message)) {c->failed=1;return AMB3R_LIMIT;}
    return AMB3R_OK;
}
static amb3r_host_v1 host(context *c) {
    return (amb3r_host_v1){AMB3R_ABI_V1,sizeof(amb3r_host_v1),c,c->caps,reg,count,emit};
}
static amb3r_status activate(context *c,const amb3r_plugin_v1 *p,const amb3r_host_v1 *h) {
    if(!p || p->abi_version!=AMB3R_ABI_V1 || p->struct_size<sizeof *p || !p->init || !p->shutdown) return AMB3R_ABI;
    char id[64];if(!copy(id,sizeof id,p->plugin_id)) return AMB3R_INVALID;
    if((p->required_capabilities&c->caps)!=p->required_capabilities) return AMB3R_DENIED;
    c->registering=1;c->failed=0;
    amb3r_status s=p->init(h);c->registering=0;
    if(s!=AMB3R_OK || c->failed || !c->command) {
        if(s==AMB3R_OK) p->shutdown();
        c->command=NULL;c->userdata=NULL;c->name[0]=0;
        return s==AMB3R_OK?AMB3R_FAILED:s;
    }
    return AMB3R_OK;
}
static amb3r_status call(context *c,const amb3r_host_v1 *h,amb3r_snapshot r) {
    if(!c->command || c->running) return AMB3R_INVALID;
    c->running=1;c->failed=0;c->code[0]=c->message[0]=0;
    amb3r_status s=c->command(h,r,c->userdata);c->running=0;
    if(s!=AMB3R_OK || c->failed) {c->code[0]=c->message[0]=0;return s==AMB3R_OK?AMB3R_FAILED:s;}
    return AMB3R_OK;
}
static amb3r_status nop(const amb3r_host_v1 *h,amb3r_snapshot r,void *u) {(void)h;(void)r;(void)u;return AMB3R_OK;}
static amb3r_status duplicate(const amb3r_host_v1 *h) {
    amb3r_status s=h->register_command(h->context,S("dup"),nop,NULL);
    if(s!=AMB3R_OK)return s;
    (void)h->register_command(h->context,S("dup"),nop,NULL);
    return AMB3R_OK; /* Host must detect sticky registration failure. */
}
static void noop(void) {}
#define REQUIRE(expr) do { if(!(expr)) {fprintf(stderr,"failed: %s\n",#expr);return 1;} } while(0)
int main(void) {
    const amb3r_plugin_v1 *p=amb3r_plugin_entry_v1();
    context c={.caps=AMB3R_CAP_READ|AMB3R_CAP_DIAGNOSTIC|AMB3R_CAP_REGISTER,.revision=9,.components=4};
    amb3r_host_v1 h=host(&c);
    amb3r_plugin_v1 wrong=*p;wrong.abi_version=99;
    REQUIRE(activate(&c,&wrong,&h)==AMB3R_ABI);
    context denied={.caps=AMB3R_CAP_READ};amb3r_host_v1 hd=host(&denied);
    REQUIRE(activate(&denied,p,&hd)==AMB3R_DENIED && !denied.command);
    amb3r_plugin_v1 dup={AMB3R_ABI_V1,sizeof dup,{"dup",3},AMB3R_CAP_REGISTER,duplicate,noop};
    REQUIRE(activate(&c,&dup,&h)==AMB3R_FAILED && !c.command);
    REQUIRE(activate(&c,p,&h)==AMB3R_OK && !strcmp(c.name,"example.count"));
    REQUIRE(call(&c,&h,8)==AMB3R_STALE && !c.code[0]);
    REQUIRE(call(&c,&h,9)==AMB3R_OK && !strcmp(c.message,"design contains 4 components"));
    printf("%s: %s\n",c.code,c.message);
    p->shutdown();c.command=NULL;c.userdata=NULL;
    REQUIRE(call(&c,&h,9)==AMB3R_INVALID);
    puts("reference SDK lifecycle, ABI, capability, stale snapshot and rollback checks passed");
    return 0;
}
