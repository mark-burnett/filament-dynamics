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

    filaments      = bindings.db_multiple(run.filaments,      parameters)
    transitions    = bindings.db_multiple(run.transitions,    parameters)
    measurements   = bindings.db_multiple(run.measurements,   parameters)
    end_conditions = bindings.db_multiple(run.end_conditions, parameters)
    concentrations = bindings.db_multiple(run.concentrations, parameters)

    return Simulation(transitions=transitions, concentrations=concentrations,
                      measurements=measurements, end_conditions=end_conditions,
                      filaments=filaments)
