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

class Concentration(object):
    @property
    def value(self):
        raise NotImplementedError()
    def remove_monomer(self):
        pass
    def add_monomer(self):
        pass

class FixedConcentration(Concentration):
    __slots__ = ['conc']
    def __init__(self, concentration=-1):
        if concentration < 0:
            raise ValueError('Negative concentrations not allowed.')
        self.concentration = concentration

    @property
    def value(self):
        return self.concentration

class ZeroConcentration(Concentration):
    @property
    def value(self):
        return 0

class FixedReagent(Concentration):
    __slots__ = ['monomer_conc', 'filament_tip_conc']
    def __init__(self, initial_concentration=None, filament_tip_concentration=None):
        self.monomer_concentration      = initial_concentration
        self.filament_tip_concentration = filament_tip_concentration

    @property
    def value(self):
        # We must ensure we never go to negative concentration.
        if self.monomer_concentration < self.filament_tip_concentration:
            return 0
        return self.monomer_concentration

    def remove_monomer(self):
        if  self.monomer_concentration >= self.filament_tip_concentration:
            self.monomer_concentration -= self.filament_tip_concentration
        else:
            raise RuntimeError(
            'Could not polymerize without going to negative concentration.')

    def add_monomer(self):
        self.monomer_concentration += self.filament_tip_concentration
