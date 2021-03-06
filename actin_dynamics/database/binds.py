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

import itertools as _itertools

from sqlalchemy import orm as _orm
from sqlalchemy.ext.associationproxy import association_proxy as _ap

from . import tables as _tables
from . import arguments as _arguments
from . import results as _results

def _create_bind(key, value):
    value.label = key
    return value

class Bind(object):
    def __init__(self, label=None, class_name=None,
                 fixed_arguments=None, variable_arguments=None):
        if label:
            self.label = label
        if class_name:
            self.class_name = class_name
        if fixed_arguments:
            self.fixed_arguments = fixed_arguments
        if variable_arguments:
            self.variable_arguments = variable_arguments

    def __repr__(self):
        return ("%s(id=%s, label='%s', class_name='%s'," +
                " fixed_arguments=%s," +
                " variable_arguments=%s)") % (
                self.__class__.__name__, self.id, self.label, self.class_name,
                dict(self.fixed_arguments),
                dict(self.variable_arguments))

    fixed_arguments = _ap('_fixed_arguments', 'value',
                          creator=_arguments.FixedArgument)
    variable_arguments = _ap('_variable_arguments', 'parameter_name',
                    creator=_arguments.VariableArgument)

_orm.mapper(Bind, _tables.bind_table,
            polymorphic_on=_tables.bind_table.c.module_name,
            properties={
    '_fixed_arguments': _orm.relationship(_arguments.FixedArgument,
        collection_class=_orm.collections.attribute_mapped_collection('name')),
    '_variable_arguments': _orm.relationship(_arguments.VariableArgument,
        collection_class=_orm.collections.attribute_mapped_collection('name'))})

class ConcentrationBind(Bind): pass
_orm.mapper(ConcentrationBind, inherits=Bind,
            polymorphic_identity='concentrations')

class TransitionBind(Bind): pass
_orm.mapper(TransitionBind, inherits=Bind, polymorphic_identity='transitions')

class EndConditionBind(Bind): pass
_orm.mapper(EndConditionBind, inherits=Bind,
            polymorphic_identity='end_conditions')

class MeasurementBind(Bind): pass
_orm.mapper(MeasurementBind, inherits=Bind, polymorphic_identity='measurements')

class FilamentBind(Bind): pass
_orm.mapper(FilamentBind, inherits=Bind, polymorphic_identity='filaments')


class AnalysisBind(Bind): pass
_orm.mapper(AnalysisBind, inherits=Bind, polymorphic_identity='analyses')


class ObjectiveBind(Bind):
    def __init__(self, data=None, *args, **kwargs):
        if data:
            self.data
        Bind.__init__(self, *args, **kwargs)

    @property
    def measurement(self):
        times  = []
        values = []
        errors = []
        for result in self.data:
            times.append(result.abscissa)
            values.append(result.ordinate)
            errors.append(result.error)

        return times, values, errors

    @measurement.setter
    def measurement(self, new_values):
        self.data = []
        for row in _itertools.izip(*new_values):
            t, v = row[:2]
            if 3 == len(row):
                e = row[3]
            elif 4 == len(row):
                e = abs(row[3] - row[2])
            elif 2 == len(row):
                e = 0
            self.data.append(_results.ObjectiveData(abscissa=t,
                                                    ordinate=v,
                                                    error=e))

_orm.mapper(ObjectiveBind, inherits=Bind, polymorphic_identity='objectives',
        properties={
            'data': _orm.relationship(_results.ObjectiveData,
                backref='objective_bind')})
