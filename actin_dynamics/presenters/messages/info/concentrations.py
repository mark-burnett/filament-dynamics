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

class ConcentrationList(object):
    __slots__ = ['data']
    def __init__(self, concentrations):
        self.data = concentrations

    @classmethod
    def from_simulation(cls, simulation):
        result = []
        for c in simulation.concentrations:
            result.append((c.id, c.state.name, c.binding.class_name, c.measurement_label.name))

        result.sort(key=operator.itemgetter(1))

        return cls(result)

class ConcentrationInfo(object):
    def __init__(self, class_name=None, state=None,
                 measurement_label=None, parameter_mappings=None,
                 state_mappings=None):
        if class_name is None:
            self.class_name = ''
        else:
            self.class_name = class_name

        if state is None:
            self.state = ''
        else:
            self.state = state

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
    def from_concentration(cls, c):
        pm = []
        for p in c.binding.parameter_mappings:
            pm.append((p.id, p.parameter_label.name, p.local_name))

        sm = []
        for s in c.binding.state_mappings:
            sm.append((s.id, s.state.name, s.local_name))

        return cls(class_name=c.binding.class_name,
                   measurement_label=c.measurement_label.name,
                   parameter_mappings=pm,
                   state_mappings=sm)
