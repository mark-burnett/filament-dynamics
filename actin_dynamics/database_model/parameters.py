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

import elixir as _elixir

from .parameter_labels import ParameterLabel as _ParameterLabel

class Parameter(_elixir.Entity):
    _elixir.using_options(tablename='parameter')

    # NOTE This is probably the most compilcated snippet of elixir code.
    label = _elixir.ManyToOne('ParameterLabel', column_kwargs=dict(index=True))
    parameter_set = _elixir.ManyToOne('ParameterSet',
                                      column_kwargs=dict(index=True))
    _elixir.using_table_options(_elixir.sqlalchemy.UniqueConstraint(
        'label_id', 'parameter_set_id'))

    value = _elixir.Field(_elixir.Float)

    @classmethod
    def from_xml(cls, element):
        pl = _ParameterLabel.get_by(name=unicode(element.get('parameter_label_name')))
        return cls(label=pl, value=float(element.get('value')))

