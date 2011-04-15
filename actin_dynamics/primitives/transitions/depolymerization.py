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

from base_classes import Transition

from actin_dynamics.numerical import rate_bisect, utils

class FixedRate(Transition):
    skip_registration = True
    __slots__ = ['state', 'rate', 'check_index', '_last_rs']
    def __init__(self, check_index=None, state=None, rate=None, label=None):
        """
        state - state to depolymerize
        rate  - depolymerization rate (constant)
        """
        self.state       = state
        self.rate        = rate
        self.check_index = check_index

        Transition.__init__(self, label=label)

    def R(self, filaments, concentrations):
        self._last_rs = []
        for filament in filaments:
            if self.state == filament[self.check_index]:
                self._last_rs.append(self.rate)
            else:
                self._last_rs.append(0)
        return sum(self._last_rs)


class BarbedDepolymerization(FixedRate):
    __slots__ = []
    def __init__(self, **kwargs):
        FixedRate.__init__(self, check_index=-1, **kwargs)

    def perform(self, time, filaments, concentrations, r):
        filament_index, remaining_r = rate_bisect.rate_bisect(r,
                list(utils.running_total(self._last_rs)))
        current_filament = filaments[filament_index]
        current_filament.shrink_barbed_end()
        concentrations[self.state].add_monomer(time)

class PointedDepolymerization(FixedRate):
    __slots__ = []
    def __init__(self, **kwargs):
        FixedRate.__init__(self, check_index=0, **kwargs)

    def perform(self, time, filaments, concentrations, r):
        filament_index, remaining_r = rate_bisect.rate_bisect(r,
                list(utils.running_total(self._last_rs)))
        current_filament = filaments[filament_index]
        current_filament.shrink_pointed_end()
        concentrations[self.state].add_monomer(time)
