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

from base_classes import Concentration

class FixedConcentration(Concentration):
    __slots__ = ['_value', 'data']
    def __init__(self, concentration=None, **kwargs):
        if concentration < 0:
            raise ValueError('Negative concentrations are nonsense.')
        self._value = float(concentration)
        Concentration.__init__(self, **kwargs)
    
    def value(self, time):
        return self._value

    def add_monomer(self):
        pass

    def remove_monomer(self):
        pass
