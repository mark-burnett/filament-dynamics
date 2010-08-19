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

from actin_dynamics import database_model as dbm

ConcentrationRequest = _nt('ConcentrationRequest', 'id')
EndConditionRequest = _nt('EndConditionRequest', 'id')
ExplicitMeasurementRequest = _nt('ExplicitMeasurementRequest', 'id')
ParameterSetRequest = _nt('ParameterSetRequest', 'id')
ParameterSetGroupRequest = _nt('ParameterSetGroupRequest', 'id')
SimulationRequest = _nt('SimulationRequest', 'id')
TransitionRequest = _nt('TransitionRequest', 'id')

class StrandFactoryRequest(object):
    def __init__(self, id):
        self.id = id

    @classmethod
    def from_simulation_id(cls, sim_id):
        sf_id = dbm.Simulation.get(sim_id).strand_factory_id
        return cls(sf_id)
