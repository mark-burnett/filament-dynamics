#    Copyright (C) 2010-2012 Mark Burnett
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

#from . import bindings
#
#from ..simulation_strategy import Simulation

#def make_run(run):
#    parameters = run.all_parameters
#
#    filament_factories = bindings.db_multiple(run.filaments,      parameters)
#    transitions        = bindings.db_multiple(run.transitions,    parameters)
#    measurements       = bindings.db_multiple(run.measurements,   parameters)
#    end_conditions     = bindings.db_multiple(run.end_conditions, parameters)
#    concentration_list = bindings.db_multiple(run.concentrations, parameters)
#
#    filaments = []
#    for ff in filament_factories:
#        filaments.extend(ff.create())
#
#    concentrations = dict((c.label, c) for c in concentration_list)
#
#    return Simulation(transitions=transitions, concentrations=concentrations,
#                      measurements=measurements, end_conditions=end_conditions,
#                      filaments=filaments)

from actin_dynamics import stochasticpy

from . import cpp_interface

def make_run(run):
    parameters = run.all_parameters

    concentrations = cpp_interface.bind_concentrations(run.concentrations,
            parameters)
    end_conditions = cpp_interface.bind_end_conditions(run.end_conditions,
            parameters)
    filaments = cpp_interface.bind_filaments(run.filaments, parameters)
    measurements = cpp_interface.bind_measurements(run.measurements, parameters)
    transitions = cpp_interface.bind_transitions(run.transitions, parameters)

    return stochasticpy.SimulationStrategy(transitions, concentrations,
            measurements, end_conditions, filaments)

# This is used for testing
def make_object_graph(object_graph, parameters):
    concentrations = cpp_interface.dict_concentrations(
            object_graph['concentrations'], parameters)
    end_conditions = cpp_interface.dict_end_conditions(
        object_graph['end_conditions'], parameters)
    filaments = cpp_interface.dict_filaments(
        object_graph['filaments'], parameters)
    measurements = cpp_interface.dict_measurements(
        object_graph['measurements'], parameters)
    transitions = cpp_interface.dict_transitions(
        object_graph['transitions'], parameters)

    return stochasticpy.SimulationStrategy(transitions, concentrations,
            measurements, end_conditions, filaments)
