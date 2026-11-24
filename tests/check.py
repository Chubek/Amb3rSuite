#!/usr/bin/env python3
import csv, json, math, sys, subprocess, tempfile
from pathlib import Path
from xml.etree import ElementTree as ET
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tools'))
from elektra_ref import run, Error
source=(root/'examples/elektra/divider.elek').read_text()
x=run(source)
assert math.isclose(x['voltages_V']['out'],6,abs_tol=1e-12)
assert math.isclose(x['voltage_source_currents_A']['V1'],-0.002,abs_tol=1e-12)
assert x['scaled_residual']<1e-12
# current sign oracle, independent ideal equation
assert math.isclose(run('circuit X { net a,g; ground g; I1: Current(g,a,2 mA); R1: Resistor(a,g,1 kohm); }')['voltages_V']['a'],2,abs_tol=1e-12)
# scale tests across resistor ratios
for i in range(1,20):
    for j in range(1,20):
        deck=source.replace('out, 1 kohm',f'out, {i} kohm').replace('gnd, 3 kohm',f'gnd, {j} kohm')
        assert math.isclose(run(deck)['voltages_V']['out'],8*j/(i+j),rel_tol=1e-12)
for bad in (source.replace('1 kohm','1 V'),source.replace('1 kohm','0 ohm'),source.replace('1 kohm','1kohm'),source.replace('1 kohm','1e999 ohm'),source.replace('R2:','R1:'),source.replace('out, gnd, 3 kohm','out, absent, 3 kohm'),source+' extra',source.replace('ground gnd','ground unused'),source.replace('vin, out, gnd','vin, out, gnd, lonely'),'circuit X { net a,b,g; ground g; R1: Resistor(a,b,1 kohm); }',(root/'examples/elektra/rc-experiment.elek.txt').read_text()):
    try:run(bad)
    except Error:pass
    else:raise AssertionError('invalid input accepted')
rows=list(csv.DictReader((root/'catalogues/kernels.csv').open()))
assert len(rows)==len({r['header_at_snapshot'] for r in rows})
assert all(r['header_at_snapshot'].startswith('mulib-') and r['header_at_snapshot'].endswith('.h') for r in rows)
for path in root.rglob('*.json'):json.loads(path.read_text())
try:
    import jsonschema
except ImportError:
    print('SKIP optional jsonschema structural validation (package absent)')
else:
    for path in (root/'schemas').glob('*.schema.json'):
        jsonschema.Draft202012Validator.check_schema(json.loads(path.read_text()))
    for n in ('plugin','project'):
        jsonschema.validate(json.loads((root/'examples'/('plugin-manifest.json' if n=='plugin' else 'project.json')).read_text()),json.loads((root/'schemas'/f'{n}.schema.json').read_text()))
    print('PASS draft schema and fixture validation')
for path in (root/'diagrams').glob('*.svg'):ET.parse(path)
subprocess.run([sys.executable,str(root/"examples/ai/broker_mock.py")],check=True)
print(f'PASS Elektra DC divider/current, 361 ratio cases, 11 rejection fixtures; {len(rows)} unique kernel entries; JSON and SVG checks')
