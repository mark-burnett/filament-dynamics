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
    description = 'Maintains a fixed concentration'
    parameters = ['concentration']
    states = None

    __slots__ = ['value', 'data']
    def __init__(self, concentration=-1, measurement_label=None):
        if concentration < 0:
            raise ValueError('Negative concentrations not allowed.')
        self.value = concentration
        self.data = [(0, concentration)]
        _Concentration.__init__(self, measurement_label)


class ZeroConcentration(_Concentration):
    description = 'Maintains zero concentration.'
    parameters = None
    states = None

    __slots__ = ['value', 'data']
    def __init__(self, measurement_label=None):
        self.value = 0
        self.data = [(0, 0)]
        _Concentration.__init__(self, measurement_label)
