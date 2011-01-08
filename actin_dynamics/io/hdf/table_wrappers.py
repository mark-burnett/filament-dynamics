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

from . import base_table_wrappers as _base_table_wrappers
from . import table_formats as _table_formats

class Measurement(_base_table_wrappers.TableWrapper):
    description = _table_formats.Measurement


class Parameters(_base_table_wrappers.DictionaryTable):
    description = _table_formats.Parameter
    key   = 'name'
    value = 'value'

    @classmethod
    def create_or_select(cls, parent_group=None):
        try:
            return cls.create(parent_group=parent_group, name='parameters')
        except:
            return cls(parent_group.parameters)

class Values(_base_table_wrappers.DictionaryTable):
    description = _table_formats.Parameter
    key   = 'name'
    value = 'value'

    @classmethod
    def create_or_select(cls, parent_group=None):
        try:
            return cls.create(parent_group=parent_group, name='values')
        except:
            return cls(parent_group.values)


# XXX Value may not be used.
class Value(_base_table_wrappers.SingleValueTable):
    column_name = 'value'
    description = _table_formats.SingleValue

class State(_base_table_wrappers.SingleValueTable):
    column_name = 'state'
    description = _table_formats.State
