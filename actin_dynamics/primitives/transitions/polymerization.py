#    Copyright (C) 2010-2011 Mark Burnett
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

import math

from base_classes import Transition

class FixedRate(Transition):
    skip_registration = True
    __slots__ = ['rate', 'species', '_last_R', '_grow_function_name']
    def __init__(self, species=None, rate=None, *args, **kwargs):
        """
        'species' that are added to the barbed end of the filament.
        'rate' is the number per second per concentration of
        """
        self.species = species
        self.rate    = rate

        Transition.__init__(self, *args, **kwargs)


    def R(self, time, state):
        value = self.rate * state.concentrations[self.species].value(time)
        self._last_R = float(value * len(state.filaments))
        return self._last_R

    def get_current_filament(self, state, r):
        bin_size = self._last_R / len(state.filaments)
        filament_index = int(r / bin_size)
        return state.filaments.values()[filament_index]

    def perform(self, time, state, r):
        current_filament = self.get_current_filament(state, r)
        getattr(current_filament, self._grow_function_name)(self.species)

        state.concentrations[self.species].remove_monomer(time)


class BarbedPolymerization(FixedRate):
    'Simple polymerization at the barbed end.'
    __slots__ = []
    def __init__(self, *args, **kwargs):
        self._grow_function_name = 'grow_barbed_end'
        FixedRate.__init__(self, *args, **kwargs)

class PointedPolymerization(FixedRate):
    'Simple polymerization at the barbed end.'
    __slots__ = []
    def __init__(self, *args, **kwargs):
        self._grow_function_name = 'grow_pointed_end'
        FixedRate.__init__(self, *args, **kwargs)
