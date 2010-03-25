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

__all__ = ['time_adjust', 'fixed_concentration']

def time_adjust(dt, rates):
    out_rates = []
    for r, s in rates:
        out_rates.append((dt*r, s))
    return out_rates

def fixed_concentration(barbed_poly_rates, pointed_poly_rates, concentrations):
    # Barbed end
    if barbed_poly_rates:
        adjusted_barbed_rates = []
        for r, s in barbed_poly_rates:
            c = concentrations[s]
            if c:
                rate = c * s
                adjusted_barbed_rates.append((rate, s))
        bpoly = simple.BarbedPoly(adjusted_barbed_rates)
        poly  = bpoly

    # Pointed end
    if pointed_poly_rates:
        adjusted_pointed_rates = []
        for r, s in pointed_poly_rates:
            c = concentrations[s]
            if c:
                rate = c * s
                adjusted_pointed_rates.append((rate, s))
        ppoly = simple.PointedPoly(adjusted_pointed_rates)
        poly  = bpoly

    # Combine if needed
    if barbed_depoly_rates and pointed_depoly_rates:
        poly   = simple.Collected_rates(bpoly, ppoly)

    return poly
