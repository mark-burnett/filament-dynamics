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

class MockExplicitMeasurement(object):
    __slots__ = ['data', 'index', 'measurement_label']
    def __init__(self, measurement_label=None, index=0, number=None):
        self.index = index
        self.measurement_label = measurement_label

        self.data = [[] for i in xrange(number)]

    def perform(self, time, values):
        for i, value in enumerate(values):
            self.data[i].append(value[self.index])
