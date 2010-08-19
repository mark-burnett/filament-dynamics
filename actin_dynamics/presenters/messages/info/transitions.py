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

from collections import namedtuple as _nt
import operator

class TransitionList(object):
    __slots__ = ['data']
    def __init__(self, parameter_sets):
        self.data = parameter_sets

    @classmethod
    def from_simulation(cls, simulation):
        result = []
        for t in simulation.transitions:
            result.append((t.id, t.name, t.binding.class_name, t.measurement_label.name))

        result.sort(key=operator.itemgetter(1))

        return cls(result)

class TransitionInfo(object):
    def __init__(self, name=None, class_name=None, measurement_label=None,
                 parameter_mappings=None, state_mappings=None):
        if name is None:
            self.name = ''
        else:
            self.name = name

        if class_name is None:
            self.class_name = ''
        else:
            self.class_name = class_name

        if measurement_label is None:
            self.measurement_label = ''
        else:
            self.measurement_label = measurement_label

        if parameter_mappings is None:
            self.parameter_mappings = []
        else:
            self.parameter_mappings = parameter_mappings

        if state_mappings is None:
            self.state_mappings = []
        else:
            self.state_mappings = state_mappings

    @classmethod
    def from_transition(cls, t):
        pm = []
        for p in t.binding.parameter_mappings:
            pm.append((p.id, p.parameter_label.name, p.local_name))

        sm = []
        for s in t.binding.state_mappings:
            sm.append((s.id, s.state.name, s.local_name))

        return cls(name=t.name, class_name=t.binding.class_name,
                   measurement_label=t.measurement_label.name,
                   parameter_mappings=pm,
                   state_mappings=sm)
