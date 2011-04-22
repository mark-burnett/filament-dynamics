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

from sqlalchemy import orm
from . import tables

__all__ = ['Argument', 'FixedArgument', 'VariableArgument']

class Argument(object): pass

orm.mapper(Argument, tables.argument_table,
           polymorphic_on=tables.argument_table.c.type)

class FixedArgument(Argument):
    def __init__(self, name, value):
        self.name  = name
        self.value = value

    def __repr__(self):
        return '%s(name=%s, value=%s)' % (
                self.__class__.__name__, self.name, self.value)

orm.mapper(FixedArgument, tables.fixed_argument_table, inherits=Argument,
           polymorphic_identity='fixed')

class VariableArgument(Argument):
    def __init__(self, name, parameter_name):
        self.name  = name
        self.parameter_name = parameter_name

    def __repr__(self):
        return '%s(name=%s, parameter_name=%s)' % (
                self.__class__.__name__, self.name, self.parameter_name)

orm.mapper(VariableArgument, tables.variable_argument_table,
           inherits=Argument, polymorphic_identity='variable')
