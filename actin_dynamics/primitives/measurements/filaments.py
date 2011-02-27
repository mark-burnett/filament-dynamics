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

from base_classes import Measurement as _Measurement

class Length(_Measurement):
    def __init__(self, label=None):
        _Measurement.__init__(self, label=label)

    def perform(self, time, filaments):
        for filament in filaments:
            length = len(filament)
            self.store(time, length, filament)

class StateCount(_Measurement):
    __slots__ = ['state']
    def __init__(self, state=None, label=None):
        self.state = state
        _Measurement.__init__(self, label=label)

    def perform(self, time, filaments):
        for filament in filaments:
            state_count = filament.state_count(self.state)
            self.store(time, state_count, filament)

class StateCountSum(_Measurement):
    __slots__ = ['base_state', 'prefix']
    def __init__(self, base_state=None, prefix=None, label=None):
        self.base_state = base_state
        self.prefix     = prefix
        _Measurement.__init__(self, label=label)

    def perform(self, time, filaments):
        for filament in filaments:
            state_count = filament.state_count(self.base_state)
            state_count += filament.state_count(self.prefix + self.base_state)
            self.store(time, state_count, filament)
