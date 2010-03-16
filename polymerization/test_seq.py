import polymerization

hr = {'t':[(0.4, 'p')], 'p':[(0.1,'d')], 'd':[]}
bp = [(0.5, 't')]
bd = {'t':0.1, 'p':0.1, 'd':0.5}

hydro  = polymerization.vectorial.Hydro(hr)
poly   = polymerization.simple.BarbedPoly(bp)
depoly = polymerization.simple.BarbedDepoly(bd)

ec = [polymerization.end_conditions.Counter(15)]

s = polymerization.Simulation(poly, depoly, hydro, {}, ec)

s.run(polymerization.CompactStrand(10, 'd'))
