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

from base_classes import Transition as _FilamentTransition

class _FixedRate(_FilamentTransition):
    skip_registration = True
    __slots__ = ['state', 'rate']
    def __init__(self, state=None, rate=None, label=None):
        """
        state - state to depolymerize
        rate  - depolymerization rate (constant)
        """
        self.state = state
        self.rate  = rate

        _FilamentTransition.__init__(self, label=None)

    def R(self, filaments, concentrations):
        result = []
        for filament in filaments:
            if self.state == filament[-1]:
                result.append(self.rate)
            else:
                result.append(0)
        return result

    def perform(self, time, filaments, concentrations, index, r):
        _FilamentTransition.perform(self, time, filaments, concentrations, index, r)

class BarbedDepolymerization(_FixedRate):
    def perform(self, time, filaments, concentrations, index, r):
        current_filament = filaments[index]
        current_filament.shrink_barbed_end()
        concentrations[self.state].add_monomer(time)
        _FixedRate.perform(self, time, filaments, concentrations, index, r)

class PointedDepolymerization(_FixedRate):
    def perform(self, time, filaments, concentrations, index, r):
        current_filament = filaments[index]
        current_filament.shrink_pointed_end()
        concentrations[self.state].add_monomer(time)
        _FixedRate.perform(self, time, filaments, concentrations, index, r)
