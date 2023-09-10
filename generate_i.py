import json

from sage.all import *

p = 21888242871839275222246405745257275088696311157297823662689037894645226208583

Fbn128base = GF(p)

bn128 = EllipticCurve(Fbn128base,[0,3])

r = bn128.order()

Fbn128 = GF(r)

x1 = Fbn128.random_element()
x2 = Fbn128.random_element() 
x3 = Fbn128.random_element()
data = {
    'x1': int(x1),
    'x2': int(x2),
    'x3': int(x3)
}

with open('input.json', 'w') as file:
    json.dump(data, file)