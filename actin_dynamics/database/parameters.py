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

__all__ = ['Parameter']

class Parameter(object):
    def __init__(self, name, value, parameter_set=None):
        self.name  = name
        self.value = value
        if parameter_set:
            self.parameter_set = parameter_set

    def __repr__(self):
        return "%s(id=%s, name='%s', value=%s)" % (
                self.__class__.__name__, self.id, self.name, self.value)

orm.mapper(Parameter, tables.parameter_table)
