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

import barbed_end

__all__ = ['fixed_concentration', 'fixed_reagents']

def fixed_concentration(parameters, concentrations,
                        free_barbed_end, free_pointed_end):
    results = []
    for s, c in concentrations.items():
        if c: # Double check for zero concentration
            if free_barbed_end:
                barbed_rate = c * parameters['barbed_polymerization'][s]
                results.append(barbed_end.FixedRate(barbed_rate, s))

            if free_pointed_end:
                raise NotImplementedError('Pointed end polymerization.')
    return results

def fixed_reagents(parameters, monomer_concentrations,
                   filament_tip_concentration,
                   free_barbed_end, free_pointed_end):
    results = []
    for s, c in monomer_concentrations.items():
        if c: # Double check for zero concentration
            if free_barbed_end:
                amount = int(c / filament_tip_concentration)
                barbed_rate = (parameters['barbed_polymerization'][s]
                               * filament_tip_concentration)
                results.append(barbed_end.FixedReagent(barbed_rate, amount, s))

            if free_pointed_end:
                raise NotImplementedError('Pointed end polymerization.')
    return results
