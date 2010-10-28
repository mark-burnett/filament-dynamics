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
    description = 'Maintains a fixed amount of the species.'
    parameters = ['initial_concentration', 'filament_tip_concentration']
    states = None

    __slots__ = ['monomer_concentration', 'filament_tip_concentration']
    def __init__(self, initial_concentration=-1,
                 filament_tip_concentration=-1,
                 label=None):
        if initial_concentration < 0:
            raise ValueError('Negative concentrations not allowed.')
        if filament_tip_concentration < 0:
            raise ValueError('Negative concentrations not allowed.')

        self.monomer_concentration = initial_concentration
        self.filament_tip_concentration = filament_tip_concentration
        _Concentration.__init__(self, label)

    @property
    def value(self):
        # We must ensure we never go to negative concentration.
        if self.monomer_concentration < self.filament_tip_concentration:
            return 0
        return self.monomer_concentration

    def add_monomer(self):
        self.monomer_concentration += self.filament_tip_concentration

    def remove_monomer(self):
        if  self.monomer_concentration >= self.filament_tip_concentration:
            self.monomer_concentration -= self.filament_tip_concentration
        else:
            raise RuntimeError(
            'Could not polymerize without going to negative concentration.')
