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

hr = {'t':[(0.4, 'p')], 'p':[(0.1,'d')], 'd':[]}
bp = [(0.5, 't')]
bd = {'t':0.1, 'p':0.1, 'd':0.5}

hydro  = polymerization.vectorial.Hydro(hr)
poly   = polymerization.simple.BarbedPoly(bp)
depoly = polymerization.simple.BarbedDepoly(bd)

ec = polymerization.end_conditions.Counter(15)

s = polymerization.Simulation(poly, depoly, hydro, {}, ec)

s.run(polymerization.CompactStrand(10, 'd'))
