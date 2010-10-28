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

import itertools
import collections

class MockTransition(object):
    def __init__(self, add_value, rate):
        self.add_value = add_value
        self.rate = rate
        self.measurements = collections.defaultdict(list)

    def R(self, filaments, concentrations):
        return list(itertools.repeat(self.rate, len(filaments)))

    def perform(self, time, filaments, concentrations, index, r):
        filaments[index][0] += self.add_value
