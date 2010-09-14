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

    __slots__ = ['measurement_label']
    def __init__(self, measurement_label=None):
        self.measurement_label = measurement_label

    def perform(self, time, strands, concentrations, index, r):
        pass


class FilamentTransition(Transition):
    skip_registration = True

    __slots__ = ['data', 'count']
    def __init__(self, number=None, measurement_label=None):
        self.count = list(itertools.repeat(0, number))
        self.data  = list(itertools.repeat([(0, 0)], number))
        Transition.__init__(self, measurement_label=measurement_label)

    def perform(self, time, strands, concentrations, index, r):
        self.count[index] += 1
        self.data[index].append((time, self.count[index]))
        Transition.perform(self, time, strands, concentrations, index, r)

class SolutionTransition(Transition):
    skip_registration = True

    __slots__ = ['data', 'count']
    def __init__(self, measurement_label=None):
        self.count = 0
        self.data  = [(0, 0)]
        Transition.__init__(self, measurement_label=measurement_label)

    def perform(self, time, strands, concentrations, index, r):
        self.count += 1
        self.data.append((time, self.count))
        Transition.perform(self, time, strands, concentrations, index, r)
