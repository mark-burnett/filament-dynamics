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
    def __call__(self):
        raise NotImplementedError()
    def initialize(self):
        pass
    def update_poly(self, event):
        pass
    def update_depoly(self, event):
        pass

class fixed_concentration(Concentration):
    __slots__ = ['conc']
    def __init__(self, conc):
        if conc < 0:
            raise ValueError('Negative concentrations not allowed.')
        self.conc = conc

    def __call__(self):
        return self.conc

class zero_concentration(Concentration):
    def __call__(self):
        return 0

class fixed_reagent(Concentration):
    __slots__ = ['initial_concentration', 'monomer_conc', 'filament_tip_conc']
    def __init__(self, initial_concentration, filament_tip_conc):
        self.initial_concentration = initial_concentration
        self.monomer_conc          = initial_concentration
        self.filament_tip_conc     = filament_tip_conc

    def __call__(self):
        return self.monomer_conc

    def initialize(self):
        self.monomer_conc = self.initial_concentration

    def update_poly(self, event):
        self.monomer_conc -= self.filament_tip_conc

    def update_depoly(self, event):
        self.monomer_conc += self.filament_tip_conc