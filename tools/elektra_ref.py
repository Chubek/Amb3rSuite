#!/usr/bin/env python3
"""Bounded Elektra DC reference profile, not the proposed full language."""
import json
import math
import re
import sys
from pathlib import Path

MAX_BYTES = 65536
MAX_UNKNOWNS = 128
MAX_PARTS = 512
TOKEN = re.compile(r'\s+|//[^\n]*|[A-Za-z_][A-Za-z_0-9]*|[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|[{}(),:;]')
IDENT = re.compile(r'[A-Za-z_][A-Za-z_0-9]*\Z')
NUMBER = re.compile(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?\Z')
UNITS = {'ohm': ('R', 1.0), 'kohm': ('R', 1e3), 'Mohm': ('R', 1e6),
         'V': ('V', 1.0), 'mV': ('V', 1e-3), 'A': ('I', 1.0), 'mA': ('I', 1e-3), 'uA': ('I', 1e-6)}
KINDS = {'Resistor': 'R', 'Voltage': 'V', 'Current': 'I'}
RESERVED = {'circuit', 'net', 'ground', *KINDS}

class Error(ValueError):
    pass

class Parser:
    def __init__(self, source):
        if len(source.encode('utf-8')) > MAX_BYTES:
            raise Error('source byte limit')
        self.tokens = []
        pos = 0
        while pos < len(source):
            m = TOKEN.match(source, pos)
            if not m:
                raise Error(f'unrecognized token at character {pos}')
            t = m.group()
            if not t.isspace() and not t.startswith('//'):
                self.tokens.append((t, pos))
            pos = m.end()
        self.tokens.append(('<eof>', pos))
        self.i = 0

    def peek(self):
        return self.tokens[self.i][0]

    def take(self):
        t = self.peek()
        if t == '<eof>':
            raise Error('unexpected end of input')
        self.i += 1
        return t

    def expect(self, t):
        if self.peek() != t:
            raise Error(f'expected {t!r} at character {self.tokens[self.i][1]}, found {self.peek()!r}')
        self.take()

    def ident(self):
        t = self.take()
        if not IDENT.fullmatch(t) or len(t) > 64 or t in RESERVED:
            raise Error(f'invalid identifier: {t}')
        return t

    def parse(self):
        self.expect('circuit'); name = self.ident(); self.expect('{'); self.expect('net')
        nets = [self.ident()]
        while self.peek() == ',':
            self.take(); nets.append(self.ident())
        self.expect(';'); self.expect('ground'); ground = self.ident(); self.expect(';')
        if len(nets) > MAX_UNKNOWNS + 1 or len(nets) != len(set(nets)) or ground not in nets:
            raise Error('invalid, duplicate, excessive or missing ground net')
        parts, used = [], set(nets)
        while self.peek() != '}':
            ref = self.ident(); self.expect(':'); kind = self.take()
            if kind not in KINDS:
                raise Error(f'unsupported device {kind}')
            self.expect('('); a = self.ident(); self.expect(','); b = self.ident(); self.expect(',')
            value_start = self.tokens[self.i][1]
            value = self.take(); unit_start = self.tokens[self.i][1]
            unit = self.take(); self.expect(')'); self.expect(';')
            if unit_start <= value_start + len(value):
                raise Error('quantity requires separated number and unit')
            if not NUMBER.fullmatch(value) or unit not in UNITS or UNITS[unit][0] != KINDS[kind]:
                raise Error(f'invalid quantity for {kind}: {value} {unit}')
            v = float(value) * UNITS[unit][1]
            if not math.isfinite(v) or (kind == 'Resistor' and (v <= 0 or not math.isfinite(1/v))):
                raise Error('nonfinite or invalid device value')
            if a == b or a not in nets or b not in nets or ref in used:
                raise Error('invalid duplicate component or terminals')
            used.add(ref); parts.append((ref, KINDS[kind], a, b, v))
            if len(parts) > MAX_PARTS:
                raise Error('component count limit')
        self.expect('}')
        if self.peek() != '<eof>' or not parts:
            raise Error('unsupported trailing syntax or empty circuit')
        return name, nets, ground, parts

def solve(a, b):
    """Scaled partial pivot Gaussian elimination; deliberately bounded reference."""
    n = len(b)
    if not n or n > MAX_UNKNOWNS:
        raise Error('matrix unknown limit')
    m = [row[:] + [rhs] for row, rhs in zip(a, b)]
    scale = [max(map(abs, row)) for row in a]
    if any(not math.isfinite(x) or x == 0 for x in scale):
        raise Error('singular or nonfinite matrix')
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(m[i][k])/scale[i])
        if abs(m[p][k]) <= 1e-14 * scale[p]:
            raise Error('singular or ill-conditioned matrix')
        m[k], m[p] = m[p], m[k]; scale[k], scale[p] = scale[p], scale[k]
        for i in range(k+1, n):
            factor = m[i][k]/m[k][k]
            m[i][k] = 0.0
            for j in range(k+1, n+1):
                m[i][j] -= factor*m[k][j]
    x = [0.0]*n
    for i in reversed(range(n)):
        x[i] = (m[i][-1] - math.fsum(m[i][j]*x[j] for j in range(i+1,n)))/m[i][i]
    if not all(map(math.isfinite, x)):
        raise Error('nonfinite solution')
    errors = []
    for row, rhs in zip(a,b):
        terms = [u*v for u,v in zip(row,x)]
        denom = max(1e-30, abs(rhs) + math.fsum(map(abs, terms)))
        errors.append(abs(math.fsum(terms)-rhs)/denom)
    residual = max(errors)
    if not math.isfinite(residual) or residual > 1e-10:
        raise Error('scaled residual exceeds reference tolerance')
    return x, residual

def run(source):
    name, nets, ground, parts = Parser(source).parse()
    ids = {k:i for i,k in enumerate(k for k in nets if k != ground)}
    branches = {ref:len(ids)+i for i,ref in enumerate(ref for ref,kind,*_ in parts if kind=='V')}
    n = len(ids)+len(branches)
    if n > MAX_UNKNOWNS:
        raise Error('matrix unknown limit')
    a = [[0.0]*n for _ in range(n)]; b = [0.0]*n
    for ref,kind,left,right,v in parts:
        i,j=ids.get(left),ids.get(right)
        if kind=='R':
            g=1/v
            for k in (i,j):
                if k is not None: a[k][k]+=g
            if i is not None and j is not None:
                a[i][j]-=g; a[j][i]-=g
        elif kind=='I':
            if i is not None: b[i]-=v
            if j is not None: b[j]+=v
        else:
            k=branches[ref]
            for row,sign in ((i,1),(j,-1)):
                if row is not None: a[row][k]+=sign; a[k][row]+=sign
            b[k]=v
    if not all(math.isfinite(v) for row in a for v in row) or not all(map(math.isfinite,b)):
        raise Error('nonfinite stamps')
    x, residual = solve(a,b)
    return {'schema':1,'profile':'elektra-ref-dc-v1','circuit':name,'voltages_V':{ground:0.0, **{k:x[i] for k,i in ids.items()}},'voltage_source_currents_A':{k:x[i] for k,i in branches.items()},'scaled_residual':residual}

def main(argv):
    if len(argv)!=2:
        print('usage: elektra_ref.py PATH',file=sys.stderr); return 2
    try:
        with Path(argv[1]).open('rb') as f:
            raw=f.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES: raise Error('source byte limit')
        print(json.dumps(run(raw.decode('utf-8')),indent=2,allow_nan=False)); return 0
    except (OSError, ValueError, ArithmeticError) as exc:
        print(f'elektra: {exc}',file=sys.stderr); return 2

if __name__=='__main__':
    sys.exit(main(sys.argv))
