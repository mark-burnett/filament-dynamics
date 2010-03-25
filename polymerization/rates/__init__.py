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
import depolymerization
import hydrolysis

def collect_time_adjusted(dt, parameters, barbed_end, pointed_end):
    """
    Extract raw rates from 'parameters' and adjust them by dt.
    """
    if barbed_end:
        barbed_poly_rates   = polymerization.time_adjust(dt,
                parameters['barbed_polymerization'])
        barbed_depoly_rates = depolymerization.time_adjust(dt,
                parameters['barbed_depolymerization'])
    else:
        barbed_poly_rates   = None
        barbed_depoly_rates = None

    if pointed_end:
        pointed_poly_rates   = polymerization.time_adjust(dt,
                parameters['pointed_polymerization'])
        pointed_depoly_rates = depolymerization.time_adjust(dt,
                parameters['pointed_depolymerization'])
    else:
        pointed_poly_rates   = None
        pointed_depoly_rates = None
    
    hydrolysis_rates = hydrolysis.time_adjust(dt,
            parameters['hydrolysis_rates'])

    return (barbed_poly_rates, pointed_poly_rates, barbed_depoly_rates,
            pointed_depoly_rates, hydrolysis_rates)
