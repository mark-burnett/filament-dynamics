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

from base_classes import Concentration as _Concentration

class FixedReagent(_Concentration):
    __slots__ = ['_value', 'monomer_count', 'concentration_per_monomer']
    def __init__(self, initial_concentration=-1,
                 filament_tip_concentration=-1,
                 number=None, label=None, sample_period=None):
        initial_concentration = float(initial_concentration)

        self.monomer_count = int(number * initial_concentration
                              / filament_tip_concentration)
        self.concentration_per_monomer = (filament_tip_concentration / number)

        self._value = self.concentration_per_monomer * self.monomer_count

        _Concentration.__init__(self, label=label)

    def value(self, time):
        return self._value

    def add_monomer(self):
        self.monomer_count += 1
        self._value = self.concentration_per_monomer * self.monomer_count

    def remove_monomer(self):
        self.monomer_count -= 1
        self._value = self.concentration_per_monomer * self.monomer_count
