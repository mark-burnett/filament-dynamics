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
    __slots__ = ['old_species', 'rate', 'new_species', 'index',
                 '_last_filaments']
    def __init__(self, index=None, old_species=None, rate=None,
                 new_species=None, label=None):
        self.index     = int(index)
        self.old_species = old_species
        self.rate      = float(rate)
        self.new_species = new_species

        Transition.__init__(self, label=label)

    def R(self, time, state):
        self._last_filaments = []
        for name, filament in state.filaments.iteritems():
            if self.old_species == filament[self.index]:
                self._last_filaments.append(filament)
        return self.rate * len(self._last_filaments)

    def get_current_filament(self, r):
        return self._last_filaments[int(r / self.rate)]

    def perform(self, time, state, r):
        current_filament = self.get_current_filament(r)
        current_filament[self.index] = self.new_species


class BarbedEndHydrolysis(EndHydrolysis):
    def __init__(self, *args, **kwargs):
        EndHydrolysis.__init__(self, index=-1, *args, **kwargs)

class PointedEndHydrolysis(EndHydrolysis):
    def __init__(self, *args, **kwargs):
        EndHydrolysis.__init__(self, index=0, *args, **kwargs)
