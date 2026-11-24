/* Pinned MuLIB C API example. Compile with -I <mulib>/include -lm.
 * Exactly one TU defines implementation switches. Not a general SPICE engine. */
#define MULIB_IMPL_ECAD_SCHEMATIC
#define MULIB_IMPL_ECAD_NETLIST
#define MULIB_IMPL_SPICE_LEXER
#define MULIB_IMPL_SPICE_NETLIST
#define MULIB_IMPL_SPICE_STAMP
#define MULIB_IMPL_SPICE_R
#define MULIB_IMPL_SPICE_C
#define MULIB_IMPL_SPICE_INDEPENDENT
#define MULIB_IMPL_NUM_DENSE
#define MULIB_IMPL_SPICE_OP
#define MULIB_IMPL_SPICE_TRAN
#define MULIB_IMPL_WAVE_SIGNAL
#include "mulib-ecad-netlist.h"
#include "mulib-spice-op.h"
#include "mulib-spice-tran.h"
#include "mulib-wave-signal.h"
#include <math.h>
#include <stdio.h>

int main(void) {
    const mulib_ecad_component_t parts[] = {
        {"V1", 'V', "in", "0", 8.0}, {"R1", 'R', "in", "out", 1000.0},
        {"R2", 'R', "out", "0", 3000.0}, {"C1", 'C', "out", "0", 1e-6}
    };
    mulib_ecad_schematic_t schematic = {0};
    mulib_spice_netlist_t net = {0};
    mulib_wave_signal_t wave = {.kind = MULIB_WAVE_ANALOG};
    char deck[512]; size_t used = 0; double volts[128], samples[80];
    int status = 1;
    for (size_t i=0; i<sizeof parts/sizeof parts[0]; ++i)
        if (!mulib_ecad_schematic_add(&schematic,&parts[i])) goto done;
    if (!mulib_ecad_netlist_write(&schematic,deck,sizeof deck,&used) ||
        !mulib_spice_netlist_parse(deck,&net,NULL)) goto done;
    int node=mulib_spice_netlist_find_node(&net,"out");
    if (node<=0 || node>UINT16_MAX) goto done;
    if (!mulib_spice_op_solve(&net,volts,128) || fabs(volts[node-1]-6.0)>1e-12) goto done;
    const double dt=75e-6;
    if (!mulib_spice_tran_fixed(&net,dt,80,(uint16_t)node,samples) ||
        !mulib_wave_signal_push(&wave,0,0)) goto done;
    for (size_t i=0;i<80;++i) {
        double expected=6*(1-pow(10.0/11.0,(double)(i+1)));
        if (!isfinite(samples[i]) || fabs(samples[i]-expected)>1e-11 ||
            !mulib_wave_signal_push(&wave,(double)(i+1)*dt,samples[i])) goto done;
    }
    printf("time_s,voltage_V\n");
    for (size_t i=0;i<wave.count;++i)
        printf("%.12g,%.12g\n",wave.samples[i].time,wave.samples[i].value);
    status=0;
done:
    mulib_wave_signal_free(&wave);
    if(status) fputs("RC chain failed\n",stderr);
    return status;
}
