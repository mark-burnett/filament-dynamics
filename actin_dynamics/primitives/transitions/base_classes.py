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

from actin_dynamics import logger as _logger
_log = _logger.getLogger(__file__)

class Transition(object):
    __metaclass__ = Registration
    registry = transition_registry
    skip_registration = True

    __slots__ = ['label']
    def __init__(self, label=None):
        self.label = label
        _log.debug('Registerring transition %s as class %s.', label,
                   self.__class__.__name__)

    def perform(self, time, filaments, concentrations, index, r):
        pass

    def initialize_measurement(self, filaments):
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
            previous_time, previous_value = measurements[-1]
            measurements.append((time, previous_value + 1))
        Transition.perform(self, time, filaments, concentrations, index, r)

    def initialize_measurement(self, filaments):
        if self.label:
            for filament in filaments:
                filament.measurements[self.label].append((0, 0))
        Transition.initialize_measurement(self, filaments)

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
