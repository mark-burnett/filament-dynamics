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

from registry import measurement_registry

class Measurement(object):
    __metaclass__ = Registration
    registry = measurement_registry
    skip_registration = True
    parameters = []
    states = []

    __slots__ = ['data', 'last_value']
    def __init__(self):
        self.data = []
        self.last_value = None

    def store(self, time, value):
        if value != self.last_value:
            self.last_value = value
            self.data.append((time, value))
