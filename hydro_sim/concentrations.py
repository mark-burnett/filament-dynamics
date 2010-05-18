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

    def value(self):
        return self.concentration

class ZeroConcentration(Concentration):
    def value(self):
        return 0

class FixedReagent(Concentration):
    __slots__ = ['monomer_conc', 'filament_tip_conc']
    def __init__(self, initial_concentration=None, filament_tip_conc=None):
        self.monomer_conc      = initial_concentration
        self.filament_tip_conc = filament_tip_conc

    def value(self):
        # We must ensure we never go to negative concentration.
        if self.monomer_conc < self.filament_tip_conc:
            return 0
        return self.monomer_conc

    def remove_monomer(self):
        if  self.monomer_conc >= self.filament_tip_conc:
            self.monomer_conc -= self.filament_tip_conc
        else:
            raise RuntimeError(
            'Could not polymerize without going to negative concentration.')

    def add_monomer(self):
        self.monomer_conc += self.filament_tip_conc
