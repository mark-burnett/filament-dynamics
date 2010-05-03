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

import copy
import kmc.simulation

__all__ = ['simulation']

def simulation(transitions, end_conditions, measuremets):
    while True:
        trans_copy = copy.deepcopy(transitions)
        ec_copy    = copy.deepcopy(end_conditions)
        meas_copy  = copy.deepcopy(measuremets)

        # Construct simulation.
        yield kmc.simulation.Simulation(trans_copy, meas_copy, ec_copy)

def sequence(simulation_generators):
    while True:
        yield kmc.simulation.SimulationSequence(
                [next(sg) for sg in simulation_generators])
