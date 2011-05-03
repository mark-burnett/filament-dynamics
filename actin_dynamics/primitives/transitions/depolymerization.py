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

from base_classes import Transition

from actin_dynamics.numerical import rate_bisect, utils

class FixedRate(Transition):
    skip_registration = True
    __slots__ = ['species', 'rate', 'check_index', '_last_rs',
                 '_last_names', '_shrink_function_name']
    def __init__(self, check_index=None, species=None, rate=None,
                 *args, **kwargs):
        """
        species - species to depolymerize
        rate  - depolymerization rate (constant)
        """
        self.species     = species
        self.rate        = rate
        self.check_index = check_index

        Transition.__init__(self, *args, **kwargs)

    def R(self, time, state):
        self._last_names = []
        self._last_rs = []
        for name, filament in state.filaments.iteritems():
            self._last_names.append(name)
            if self.species == filament[self.check_index]:
                self._last_rs.append(self.rate)
            else:
                self._last_rs.append(0)
        return sum(self._last_rs)


    def perform(self, time, state, r):
        filament_index, remaining_r = rate_bisect.rate_bisect(r,
                list(utils.running_total(self._last_rs)))
        name = self._last_names[filament_index]
        current_filament = state.filaments[name]

        getattr(current_filament, self._shrink_function_name)()
        if not len(current_filament):
            del filaments[name]

        state.concentrations[self.species].add_monomer(time)


class BarbedDepolymerization(FixedRate):
    __slots__ = []
    def __init__(self, *args, **kwargs):
        self._shrink_function_name = 'shrink_barbed_end'
        FixedRate.__init__(self, check_index=-1, *args, **kwargs)

class PointedDepolymerization(FixedRate):
    __slots__ = []
    def __init__(self, *args, **kwargs):
        self._shrink_function_name = 'shrink_pointed_end'
        FixedRate.__init__(self, check_index=0, *args, **kwargs)
