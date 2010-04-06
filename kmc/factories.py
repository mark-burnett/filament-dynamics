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

import predicates
import transitions
import end_conditions
import data_collectors

import simulation

__all__ = ['build_depolymerization_simulation']

def build_depolymerization_simulation(model_type,
                                      model_parameters,
                                      polymerization_duration,
                                      depolymerization_duration,
                                      polymerization_concentrations,
                                      barbed_end=True, pointed_end=False):
    # Make poly and depoly transition objects
    poly_trans = build_polymerization_transitions(model_parameters,
                                                  polymerization_concentrations,
                                                  barbed_end, pointed_end)
    depoly_trans = build_depolymerization_transitions(model_parameters,
                                                      barbed_end, pointed_end)

    # Make hydrolysis transition objects
    hydro_trans = build_hydrolysis_transitions(model_type, model_parameters)

    # Make end conditions
    poly_ecs = end_conditions.RandomMaxVariable('sim_time',
                                                polymerization_duration)
    depoly_ecs = end_conditions.MaxVariable('sim_time',
                                            depolymerization_duration)

    # Make data collectors
    poly_dcs = {}
    depoly_dcs = {'length':data_collectors.strand_length,
                  'time':  data_collectors.Variable('sim_time')}

    return simulation.SimulationSequence([
        simulation.Simulation(poly_trans + depoly_trans + hydro_trans,
                              poly_ecs, poly_dcs),
        simulation.Simulation(depoly_trans + hydro_trans,
                              depoly_ecs, depoly_dcs)])

def build_polymerization_transitions(parameters, concentrations,
                                     barbed_end, pointed_end):
    results = []
    for s, c in concentrations.items():
        if c: # Double check for zero concentration
            if barbed_end:
                barbed_rate = c * parameters['barbed_polymerization'][s]
                results.append(transitions.BarbedPolymerization(barbed_rate, s))
            if pointed_end:
                pointed_rate = c * parameters['pointed_polymerization'][s]
                results.append(transitions.PointedPolymerization(pointed_rate, s))
    return results

def build_depolymerization_transitions(parameters, barbed_end, pointed_end):
    results = []
    if barbed_end:
        results.append(transitions.BarbedDepolymerization(
            parameters['barbed_depolymerization']))
    if pointed_end:
        results.append(transitions.PointedDepolymerization(
            parameters['pointed_depolymerization']))
    return results

def random_hydrolysis_transitions(parameters):
    results = []
    for state, (rate, out) in parameters['hydrolysis_rates'].items():
        results.append(transitions.Transition(predicates.Random(state), rate, out))
    return results

def cooperative_hydrolysis_transitions(parameters):
    results = []
    for state, data in parameters['hydrolysis_rates'].items():
        for neighbor, (rate, out) in data.items():
            results.append(transitions.Transition(
                    predicates.Cooperative(state, neighbor), rate, out))
    return results

def build_hydrolysis_transitions(model_type, parameters):
    dispatch = {'random':      random_hydrolysis_transitions,
                'vectorial':   cooperative_hydrolysis_transitions,
                'cooperative': cooperative_hydrolysis_transitions,
                'lipowsky':    cooperative_hydrolysis_transitions}
    return dispatch[model_type](parameters)
