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

class FixedRate(Transition):
    skip_registration = True
    __slots__ = ['rate', 'state', '_last_R']
    def __init__(self, state=None, rate=None, label=None):
        """
        'state' that are added to the barbed end of the filament.
        'rate' is the number per second per concentration of
        """
        self.state = state
        self.rate  = rate

        Transition.__init__(self, label=label)

    def R(self, filaments, concentrations):
        value = self.rate * concentrations[self.state].value
        self._last_R = value * len(filaments)
        return self._last_R


class BarbedPolymerization(FixedRate):
    'Simple polymerization at the barbed end.'
    def perform(self, time, filaments, concentrations, r):
        index = int(r / self._last_R)
        current_filament = filaments[index]
        current_filament.grow_barbed_end(self.state)
        concentrations[self.state].remove_monomer(time)

class PointedPolymerization(FixedRate):
    'Simple polymerization at the barbed end.'
    def perform(self, time, filaments, concentrations, r):
        index = int(r / self._last_R)
        current_filament = filaments[index]
        current_filament.grow_pointed_end(self.state)
        concentrations[self.state].remove_monomer(time)
