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

from base_classes import Transition

class EndHydrolysis(Transition):
    __slots__ = ['old_state', 'rate', 'new_state', 'index', '_last_R']
    def __init__(self, index=None, old_state=None, rate=None,
                 new_state=None, label=None):
        self.index     = int(index)
        self.old_state = old_state
        self.rate      = float(rate)
        self.new_state = new_state

        Transition.__init__(self, label=label)

    def R(self, filaments, concentrations):
        num_filaments = sum(self.old_state == f[self.index] for f in filaments)
        self._last_R = self.rate * num_filaments
        return self._last_R

    def perform(self, time, filaments, concentrations, r):
        filament_index = int(r / self._last_R)
        current_filament = filaments[filament_index]
        current_filament[self.index] = self.new_state


class BarbedEndHydrolysis(EndHydrolysis):
    def __init__(self, *args, **kwargs):
        EndHydrolysis.__init__(self, index=-1, *args, **kwargs)

class PointedEndHydrolysis(EndHydrolysis):
    def __init__(self, *args, **kwargs):
        EndHydrolysis.__init__(self, index=0, *args, **kwargs)
