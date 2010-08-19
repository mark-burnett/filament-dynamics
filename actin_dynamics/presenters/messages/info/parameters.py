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

import operator

class ParameterSet(object):
    __slots__ = ['data']
    def __init__(self, parameters):
        self.data = parameters

    @classmethod
    def from_parameter_set(cls, parameter_set):
        result = []
        for par in parameter_set.parameters:
            result.append((par.id, par.label.name, par.value))

        result.sort(key=operator.itemgetter(1))

        return cls(result)

    @classmethod
    def from_simulation(cls, simulation):
        result = []

        result.extend(_get_pars_from_binding(simulation.strand_factory.binding))

        for t in simulation.transitions:
            result.extend(_get_pars_from_binding(t.binding))

        for c in simulation.concentrations:
            result.extend(_get_pars_from_binding(c.binding))

        for ec in simulation.end_conditions:
            result.extend(_get_pars_from_binding(ec.binding))

        for em in simulation.explicit_measurements:
            result.extend(_get_pars_from_binding(em.binding))

        result.sort(key=operator.itemgetter(1))
        
        return cls(result)


class ParameterSetList(object):
    __slots__ = ['parameter_sets']
    def __init__(self, parameter_sets):
        self.parameter_sets = parameter_sets

    @classmethod
    def from_parameter_set_group(cls, psg):
        result = []
        for ps in psg.parameter_sets:
            result.append((ps.id, ps.name))

        result.sort(key=operator.itemgetter(1))

        return cls(result)


class ParameterSetGroupList(object):
    __slots__ = ['parameter_set_groups']
    def __init__(self, parameter_set_groups):
        self.parameter_set_groups = parameter_set_groups

    @classmethod
    def from_simulation(cls, simulation):
        result = []
        for psg in simulation.parameter_set_groups:
            result.append((psg.id, psg.name))

        result.sort(key=operator.itemgetter(1))

        return cls(result)


def _get_pars_from_binding(binding):
    result = []
    for pm in binding.parameter_mappings:
        pml = pm.parameter_label
        result.append((pml.id, pml.name, ''))
    return result
