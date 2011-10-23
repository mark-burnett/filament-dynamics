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

from base_classes import FilamentTransition as _FilamentTransition
from . import mixins as _mixins

class EndHydrolysis(_FilamentTransition):
    __slots__ = ['old_state', 'rate', 'new_state']
    def __init__(self, index=None, old_state=None, rate=None, new_state=None,
            label=None):
        self.index     = int(index)
        self.old_state = old_state
        self.rate      = float(rate)
        self.new_state = new_state

        _FilamentTransition.__init__(self, label=label)

    def R(self, time, filaments, concentrations):
        results = []
        for filament in filaments:
            if filament.states and self.old_state == filament[self.index]:
                results.append(self.rate)
            else:
                results.append(0)
        return results
#        num_filaments = sum(self.old_state == f[self.index] for f in filaments)
#        return [self.rate * num_filaments]

    def perform(self, time, filaments, concentrations, filament_index, r):
        current_filament = filaments[filament_index]
        current_filament[self.index] = self.new_state

        _FilamentTransition.perform(self, time, filaments, concentrations,
                                    filament_index, r)

class BarbedEndHydrolysis(EndHydrolysis):
    def __init__(self, *args, **kwargs):
        EndHydrolysis.__init__(self, index=-1, *args, **kwargs)

class PointedEndHydrolysis(EndHydrolysis):
    def __init__(self, *args, **kwargs):
        EndHydrolysis.__init__(self, index=0, *args, **kwargs)

BarbedEndHydrolysisWIthByproduct = _mixins.add_byproduct(BarbedEndHydrolysis)
PointedEndHydrolysisWIthByproduct = _mixins.add_byproduct(PointedEndHydrolysis)
