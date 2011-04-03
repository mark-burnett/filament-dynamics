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

from ..meta_classes import Registration

from registry import concentration_registry

class Concentration(object):
    __metaclass__ = Registration
    registry = concentration_registry
    skip_registration = True

    __slots__ = ['label', 'sample_period', 'data']
    def __init__(self, sample_period=None, label=None):
        self.label = label
        self.sample_period = sample_period
        self.data  = [[0, self.value]]

    def add_monomer(self, time):
        self.update_measurement(time)

    def remove_monomer(self, time):
        self.update_measurement(time)

    def update_measurement(self, time):
#        if self.value != self.data[-1][1]:
#            self.data.append((time, self.value))
        last_time, last_value = self.data[-1]
        if time <= last_time:
            self.data[-1][1] = self.value
        else:
            self.data.append([time + self.sample_period, self.value])
