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

class StateCounts(_Measurement):
    def __init__(self, label=None):
        _Measurement.__init__(self, label=label)

    def perform(self, time, filaments):
        for filament in filaments:
            states = filament.containted_states()
            state_counts = dict((state, filament.state_count(state))
                                for state in states)
            self.store(time, state_counts, filament)
