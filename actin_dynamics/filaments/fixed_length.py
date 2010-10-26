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

from base_classes import FilamentFactory as _FilamentFactory

from .single_strand import Filament

class SingleState(_FilamentFactory):
    description = 'Creates strands of a fixed state and length.'
    states = ['state']
    parameters = ['length']

    def __init__(self, state, length):
        self.state = state
        self.length = int(length)

    def create(self):
        return Filament(itertools.repeat(self.state, self.length))

class SingleStateFromConcentrations(SingleState):
    parameters = ['concentration', 'filament_tip_concentration']
    def __init__(self, state, concentration, filament_tip_concentration):
        length = int(seed_concentration / filament_tip_concentration)
        SingleState.__init__(self, state, length)

class NormalDistribution(_FilamentFactory):
    def __init__(self, mean=None, standard_deviation=None,
                 initial_state=None, number=None):
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.initial_state = initial_state
        self.number = number

    def create(self):
        # XXX Write this.
        return []
