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

import collections

import polymerization.factories   as pf
import depolymerization.factories as df
import hydrolysis.factories       as hf

import end_conditions
import data_collectors

import simulation

__all__ = ['build_initial_strand', 'build_depolymerization_simulation']

def build_initial_strand(size, state, free_barbed_end, free_pointed_end):
    type = list
    if free_pointed_end:
        type = collections.deque
    return type(state for i in xrange(size))

def build_depolymerization_simulation(model_type,
                                      model_parameters,
                                      polymerization_duration,
                                      depolymerization_duration,
                                      polymerization_concentrations,
                                      free_barbed_end,
                                      free_pointed_end):
    # Make poly and depoly transition objects
    poly_trans   = pf.fixed_concentration(model_parameters,
                                          polymerization_concentrations,
                                          free_barbed_end, free_pointed_end)
    depoly_trans = df.fixed_rates(model_parameters,
                                  free_barbed_end, free_pointed_end)
    # Make hydrolysis transition objects
    hydro_trans  = hf.constant_rates(model_type,
                                     model_parameters['hydrolysis_rates'],
                                     free_barbed_end, free_pointed_end)

    # Make end conditions
    poly_ecs = end_conditions.RandomMaxVariable('sim_time',
                                                polymerization_duration)
    depoly_ecs = end_conditions.MaxVariable('sim_time',
                                            depolymerization_duration)

    # Make data collectors
    poly_dcs = {}
    depoly_dcs = {'length': data_collectors.strand_length,
                  'time':   data_collectors.Variable('sim_time')}

    return simulation.SimulationSequence([
        simulation.Simulation(poly_trans + depoly_trans + hydro_trans,
                              poly_ecs, poly_dcs),
        simulation.Simulation(depoly_trans + hydro_trans,
                              depoly_ecs, depoly_dcs)])

def build_cleavage_simulation(model_type,
                              model_parameters,
                              duration,
                              transition_from,
                              monomer_concentrations,
                              filament_tip_concentration,
                              free_barbed_end,
                              free_pointed_end):
    # Make poly and depoly transition objects
    poly   = pf.fixed_reagents(model_parameters,
                               monomer_concentrations,
                               filament_tip_concentration,
                               free_barbed_end, free_pointed_end)
    depoly = df.fixed_rates(model_parameters, free_barbed_end, free_pointed_end)

    # Make hydrolysis transition objects
    hydro_rates = {}
    hydro_rates[transition_from] = \
                       model_parameters['hydrolysis_rates'][transition_from]
    hydro  = hf.constant_rates(model_type, hydro_rates,
                               free_barbed_end, free_pointed_end)

    # Make end conditions
    ecs = end_conditions.MaxVariable('sim_time', duration)

    # Make data collectors
    dcs = {'length':       data_collectors.strand_length,
           'time':         data_collectors.Variable('sim_time'),
           'hydro_events': data_collectors.EventCounter('hydrolysis')}

    return simulation.Simulation(poly + depoly + hydro, ecs, dcs)
