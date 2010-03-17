#    Copyright (C) 2010 Mark Burnett
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import polymerization
import mp_sim

hr = {'t':[(0.4, 'p')], 'p':[(0.1,'d')], 'd':[]}
bp = [(0.5, 't')]
bd = {'t':0.1, 'p':0.1, 'd':0.5}

hydro  = polymerization.vectorial.Hydro(hr)
poly   = polymerization.simple.BarbedPoly(bp)
depoly = polymerization.simple.BarbedDepoly(bd)

ec = polymerization.end_conditions.Counter(100000)

build_sim = polymerization.Simulation(poly, depoly, hydro, {}, ec)
wash_sim  = polymerization.Simulation(polymerization.simple.NoOp, depoly,
                                      hydro, {}, ec)

combined_sim = polymerization.SimulationSequence([build_sim, wash_sim])

results = mp_sim.pool_sim(combined_sim, polymerization.CompactStrand(10, 'd'),
                          16)

# Separate first and second stages.
results = zip(*results)
print results[0]
print
print
print results[1]
