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

class MockTransition(object):
    def __init__(self, add_value, rate, measurement_label=None):
        self.add_value = add_value
        self.rate = rate
        self.measurement_label = measurement_label

    def R(self, strand, concentrations):
        return self.rate

    def perform(self, time, strand, concentrations, r):
        strand[0] += self.add_value
