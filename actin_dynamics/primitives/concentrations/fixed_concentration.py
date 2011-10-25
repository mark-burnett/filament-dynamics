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

class FixedConcentration(_Concentration):
    __slots__ = ['value', 'data']
    def __init__(self, concentration=-1, **kwargs):
        if concentration < 0:
            raise ValueError('Negative concentrations not allowed.')
        self.value = float(concentration)
        _Concentration.__init__(self, **kwargs)

    def add_monomer(self, time):
        pass

    def remove_monomer(self, time):
        pass


class ZeroConcentration(_Concentration):
    __slots__ = ['value', 'data', 'monomer_count']
    def __init__(self, **kwargs):
        self.value = 0
        self.monomer_count = 0
        _Concentration.__init__(self, **kwargs)

    def add_monomer(self, time):
        pass

    def remove_monomer(self, time):
        pass
