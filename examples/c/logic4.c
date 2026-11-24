/* Pinned native MuLIB example: scalar 4-state truth values. */
#define MULIB_IMPL_DSIM_LOGIC4
#include "mulib-dsim-logic4.h"
#include <stdio.h>
int main(void) {
    if (mulib_dsim_and(MULIB_DSIM_0,MULIB_DSIM_X)!=MULIB_DSIM_0 ||
        mulib_dsim_resolve(MULIB_DSIM_0,MULIB_DSIM_1)!=MULIB_DSIM_X ||
        mulib_dsim_resolve(MULIB_DSIM_Z,MULIB_DSIM_1)!=MULIB_DSIM_1) return 1;
    puts("4-state reference passed");return 0;
}
