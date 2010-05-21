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

import itertools

from . import simulation_state

class SimulationSequence(object):
    def __init__(self, simulations, concentrations):
        self.simulations    = simulations
        self.concentrations = concentrations

    def __call__(self, initial_strand):
        return self.run(initial_strand)

    def run(self, initial_strand):
        sequence = initial_strand
        data = []
        for s, c in itertools.izip(self.simulations,
                                   self.concentrations):
            state, sim_data = s.run(simulation_state.SimulationState(sequence, c))
            data.append(sim_data)
            sequence = state.strand
        return data
