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

class StrandLength(_Measurement):
    def __init__(self, label=None):
        _Measurement.__init__(self, label=label)

    def perform(self, time, filaments):
        for filament in filaments:
            self.store(time, len(filament), filament)

class Flourescence(_Measurement):
    def __init__(self, label=None, **kwargs):
        self.state_strengths = kwargs
        _Measurement.__init__(self, label=label)

    def perform(self, time, filaments):
        for filament in filaments:
            value = self._get_flourescence(filament)
            self.store(time, value, filament)

    def _get_flourescence(self, filament):
        return sum(self.state_strengths[state] * filament.state_indices[state]
                   for state in filament.states.keys())
