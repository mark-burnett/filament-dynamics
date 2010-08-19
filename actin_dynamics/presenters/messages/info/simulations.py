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

from collections import namedtuple as _nt
import operator

from actin_dynamics import database_model as dbm

class SimulationInfo(object):
    __slots__ = ['id', 'name', 'description', 'timestamp', 'num_par_sets', 'num_runs']
    def __init__(self, id, name, description, timestamp, num_par_sets, num_runs):
        self.id = id
        self.name = name
        self.description = description
        self.timestamp = timestamp
        self.num_par_sets = num_par_sets
        self.num_runs = num_runs

    @classmethod
    def from_simulation(cls, simulation):
        id = simulation.id
        name = simulation.name
        timestamp = simulation.creation_date
        description = simulation.description
        num_par_sets = sum(
                dbm.ParameterSet.query.filter_by(parameter_set_group=psg).count()
                           for psg in simulation.parameter_set_groups)
        num_runs = sum(
                dbm.SimulationResult.query.filter_by(parameter_set=ps).count()
                       for psg in simulation.parameter_set_groups
                       for ps in psg.parameter_sets)

        return cls(id, name, description, timestamp, num_par_sets, num_runs)

class SimulationList(object):
    __slots__ = ['data']
    def __init__(self, simulations):
        self.data = simulations

    @classmethod
    def all(cls):
        result = []
        for sim in dbm.Simulation.query.all():
            result.append((sim.id, sim.name, sim.description))

        result.sort(key=operator.itemgetter(1))

        return cls(result)
