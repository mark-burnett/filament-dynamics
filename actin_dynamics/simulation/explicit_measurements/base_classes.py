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

from ..meta_classes import Registration

from registry import measurement_registry

class Measurement(object):
    __metaclass__ = Registration
    registry = measurement_registry
    skip_registration = True
    parameters = []
    states = []

    __slots__ = ['data', 'last_values']
    def __init__(self, number=None):
        self.data = [[] for i in xrange(number)]
        self.last_values = list(itertools.repeat(None, number))

    def store(self, time, values):
        for i, value in enumerate(values):
            if value != self.last_values[i]:
                self.last_values[i] = value
                self.data[i].append((time, value))
