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

from registry import transition_registry

class Transition(object):
    __metaclass__ = Registration
    registry = transition_registry
    skip_registration = True

    __slots__ = ['label']
    def __init__(self, label=None):
        self.label = label

    def perform(self, time, filaments, concentrations, index, r):
        pass


class FilamentTransition(Transition):
    skip_registration = True

    __slots__ = ['data', 'count']
    def __init__(self, label=None):
        Transition.__init__(self, label=label)

    def perform(self, time, filaments, concentrations, index, r):
        # Store data with each filament
        if self.label:
            filament = filaments[index]
            measurements = filament.measurements[self.label]
            if measurements:
                previous_time, previous_value = measurements[-1]
            else:
                previous_value = 0
            measurements.append((time, previous_value + 1))
        Transition.perform(self, time, filaments, concentrations, index, r)

class SolutionTransition(Transition):
    skip_registration = True

    __slots__ = ['data', 'count']
    def __init__(self, label=None):
        self.count = 0
        self.data  = [(0, 0)]
        Transition.__init__(self, label=label)

    def perform(self, time, filaments, concentrations, index, r):
        self.count += 1
        self.data.append((time, self.count))
        Transition.perform(self, time, filaments, concentrations, index, r)
