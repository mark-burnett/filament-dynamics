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

import simple

__all__ = ['time_adjust', 'independent']

def time_adjust(dt, rates):
    out_rates = {}
    for s, r in rates.items():
        out_rates[s] = dt * r
    return out_rates

def independent(barbed_depoly_rates, pointed_depoly_rates):
    # Barbed end
    if barbed_depoly_rates:
        bdepoly = simple.BarbedDepoly(barbed_depoly_rates)
        depoly  = bdepoly

    # Pointed end
    if pointed_depoly_rates:
        pdepoly = simple.PointedDepoly(pointed_depoly_rates)
        depoly  = pdepoly

    # Combine if needed
    if barbed_depoly_rates and pointed_depoly_rates:
        depoly = simple.Collected_rates(bdepoly, pdepoly)

    return depoly
