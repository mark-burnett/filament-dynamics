#    Copyright (C) 2011 Mark Burnett
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

from .base_classes import FilamentTransition as _FilamentTransition
from . import mixins as _mixins

class ReverseRelease(_FilamentTransition):
    __slots__ = ['old_state', 'rate', 'concentration', 'new_state', 'disable_time']
    def __init__(self, old_state=None, rate=None, new_state=None,
            disable_time=999999999, concentration=None, label=None):
        self.old_state = old_state
        self.rate      = rate
        self.new_state = new_state
        self.concentration = concentration
        self.disable_time = float(disable_time)

        _FilamentTransition.__init__(self, label=label)

    def R(self, time, filaments, concentrations):
        if time < self.disable_time:
            r = self.rate * concentrations[self.concentration].value
            return [r * filament.state_count(self.old_state)
                    for filament in filaments]
        else:
            return [0 for f in filaments]

    def perform(self, time, filaments, concentrations, filament_index, r):
        last_r = self.rate * concentrations[self.concentration].value
        target_index = int(r / last_r)
        current_filament = filaments[filament_index]
        state_index = current_filament.state_index(self.old_state, target_index)

        current_filament[state_index] = self.new_state
        concentrations[self.concentration].remove_monomer(time)

        _FilamentTransition.perform(self, time, filaments, concentrations,
                                    filament_index, r)

class BarbedTipReverseRelease(_FilamentTransition):
    __slots__ = ['old_state', 'rate', 'concentration', 'new_state', 'disable_time']
    def __init__(self, old_state=None, rate=None, new_state=None,
            disable_time=999999999, concentration=None, label=None):
        self.old_state = old_state
        self.rate      = rate
        self.new_state = new_state
        self.concentration = concentration
        self.disable_time = float(disable_time)

        _FilamentTransition.__init__(self, label=label)

    def R(self, time, filaments, concentrations):
        if time < self.disable_time:
            r = self.rate * concentrations[self.concentration].value
            result = []
            for filament in filaments:
                if self.old_state == filament[-1]:
                    result.append(r)
                else:
                    result.append(0)
            return result
        else:
            return [0 for f in filaments]

    def perform(self, time, filaments, concentrations, filament_index, r):
        last_r = self.rate * concentrations[self.concentration].value
        target_index = int(r / last_r)
        current_filament = filaments[filament_index]

        current_filament[-1] = self.new_state
        concentrations[self.concentration].remove_monomer(time)

        _FilamentTransition.perform(self, time, filaments, concentrations,
                                    filament_index, r)


class PointedTipReverseRelease(_FilamentTransition):
    __slots__ = ['old_state', 'rate', 'concentration', 'new_state', 'disable_time']
    def __init__(self, old_state=None, rate=None, new_state=None,
            disable_time=999999999, concentration=None, label=None):
        self.old_state = old_state
        self.rate      = rate
        self.new_state = new_state
        self.concentration = concentration
        self.disable_time = float(disable_time)

        _FilamentTransition.__init__(self, label=label)

    def R(self, time, filaments, concentrations):
        if time < self.disable_time:
            r = self.rate * concentrations[self.concentration].value
            result = []
            for filament in filaments:
                if self.old_state == filament[0]:
                    result.append(r)
                else:
                    result.append(0)
            return result
        else:
            return [0 for f in filaments]

    def perform(self, time, filaments, concentrations, filament_index, r):
        last_r = self.rate * concentrations[self.concentration].value
        target_index = int(r / last_r)
        current_filament = filaments[filament_index]

        current_filament[0] = self.new_state
        concentrations[self.concentration].remove_monomer(time)

        _FilamentTransition.perform(self, time, filaments, concentrations,
                                    filament_index, r)
