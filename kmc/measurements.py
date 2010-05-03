#    Copyright (C) 2009 Mark Burnett
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

class StateMeasurement(object):
    __slots__ = ['label', 'data']
    def __init__(self, label):
        self.label = label

    def initialize(self, pub, state):
        self.data = []
        self.perform(0, state)
    
    def perform(self, time, state):
        self.data.append((time, self.function(time, state)))

    def function(self, time, state):
        raise NotImplementedError()

class Length(StateMeasurement):
    def function(self, time, state):
        return len(state)
