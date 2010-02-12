from simulation import Simulation
from simple import CollectedRates, BarbedPoly, BarbedDepoly, NoOp
from sequential import Hydro

from fitpy.end_conditions import Counter

hr = {'t':[(0.4, 'p')], 'p':[(0.1,'d')], 'd':[]}
bp = [(0.5, 't')]
bd = {'t':0.1, 'p':0.1, 'd':0.5}

hydro  = Hydro(hr, 'd')
poly   = CollectedRates(BarbedPoly(bp), NoOp)
depoly = CollectedRates(BarbedDepoly(bd), NoOp)

ec = [Counter(15)]

s = Simulation(poly, depoly, hydro, {}, ec)

s.run(10)
