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

class MockConcentration(object):
    __slots__ = ['count', 'value_access_count', '_value']
    def __init__(self, count=0, value=None):
        self.count = count
        self.value_access_count = 0
        self._value = value

    @property
    def value(self):
        self.value_access_count += 1
        return self._value

    def add_monomer(self):
        self.count += 1

    def remove_monomer(self):
        self.count -= 1
