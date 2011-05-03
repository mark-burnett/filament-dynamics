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

class MockConcentration(object):
    def __init__(self, count=0, value=0):
        self._count = count
        self.value_access_count = 0
        self.monomer_access_count = 0
        self._value = value

    def value(self, time):
        self.value_access_count += 1
        return self._value

    @property
    def count(self):
        return self.monomer_count(None)

    def monomer_count(self, time):
        self.monomer_access_count += 1
        return self._count

    def add_monomer(self, time):
        self._count += 1

    def remove_monomer(self, time):
        self._count -= 1
