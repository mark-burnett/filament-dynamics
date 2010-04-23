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

__all__ = ['normal']

def single_fixed_concentration(model_model_pars, state, pars,
                               free_barbed_end, free_pointed_end):
    results = []
    c = pars['concentration']

    if c: # Double check for zero concentration
        if free_barbed_end:
            barbed_rate = c * model_model_pars['barbed_polymerization'][state]
            results.append(barbed_end.FixedRate(barbed_rate, state))

        if free_pointed_end:
            raise NotImplementedError('Pointed end polymerization.')

    return results

def single_fixed_reagent(model_model_pars, state, pars,
                         free_barbed_end, free_pointed_end):
    c                          = pars['monomer_concentration']
    filament_tip_concentration = pars['filament_tip_concentration']
    results = []
    if c: # Double check for zero concentration
        if free_barbed_end:
            amount = int(c / filament_tip_concentration)
            barbed_rate = (model_model_pars['barbed_polymerization'][state]
                           * filament_tip_concentration)
            results.append(barbed_end.FixedReagent(barbed_rate, amount, state))

        if free_pointed_end:
            raise NotImplementedError('Pointed end polymerization.')
    return results

_factory_dispatch = {'fixed_concentration': single_fixed_concentration,
                     'fixed_reagent':      single_fixed_reagent}

def normal(model_model_pars, poly_model_pars, free_barbed_end, free_pointed_end):
    results = []
    for state, pars in poly_model_pars.items():
        results.extend(_factory_dispatch[pars['type']](model_model_pars,
                                                       state, pars,
                                                       free_barbed_end,
                                                       free_pointed_end))
    return results
