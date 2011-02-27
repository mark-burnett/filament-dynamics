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

from . import bindings

from ..simulation_strategy import Simulation

def make_run(run):
    parameters = run.all_parameters

    filament_factories = bindings.db_multiple(run.filaments,      parameters)
    transitions        = bindings.db_multiple(run.transitions,    parameters)
    measurements       = bindings.db_multiple(run.measurements,   parameters)
    end_conditions     = bindings.db_multiple(run.end_conditions, parameters)
    concentration_list = bindings.db_multiple(run.concentrations, parameters)

    filaments = []
    for ff in filament_factories:
        filaments.extend(ff.create())

    concentrations = dict((c.label, c) for c in concentration_list)

    return Simulation(transitions=transitions, concentrations=concentrations,
                      measurements=measurements, end_conditions=end_conditions,
                      filaments=filaments)
