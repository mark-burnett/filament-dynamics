#    Copyright (C) 2009 Mark Burnett
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

from kmc.measurement import SimpleMeasurement, ChangingMeasurement

class StrandLength(ChangingMeasurement):
    def perform(self, time, sim_state):
        self.append(time, len(sim_state.strand))

class StrandCount(ChangingMeasurement):
    __slots__ = ['_species']
    def __init__(self, label, species):
        self._species = species
        ChangingMeasurement.__init__(self, label)

    def perform(self, time, sim_state):
        self.append(time, len(sim_state.strand.state_indices[self._species]))

class TransitionCount(SimpleMeasurement):
    __slots__ = ['old_state', 'new_state', 'count',
                 '_last_old_count', '_last_new_count']
    def __init__(self, label, old_state, new_state):
        self.old_state = old_state
        self.new_state = new_state

        self.count = 0

        self._last_old_count = -1
        self._last_new_count = -1
        SimpleMeasurement.__init__(self, label, [(0, 0)])

    def perform(self, time, sim_state):
        old_count = len(sim_state.strand.state_indices[self.old_state])
        new_count = len(sim_state.strand.state_indices[self.new_state])

        if (self._last_old_count - 1 == old_count and
            self._last_new_count + 1 == new_count):
            self.count += 1
            self.append(time, self.count)
        self._last_old_count = old_count
        self._last_new_count = new_count

class Concentration(ChangingMeasurement):
    __slots__ = ['species']
    def __init__(self, label, species):
        self.species = species
        ChangingMeasurement.__init__(self, label)

    def perform(self, time, sim_state):
        self.append(time, sim_state.concentrations[self.species].value)
