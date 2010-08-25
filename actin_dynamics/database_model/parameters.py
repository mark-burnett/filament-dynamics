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

class ParameterLabel(_elixir.Entity):
    _elixir.using_options(tablename='parameter_label')

    name = _elixir.Field(_elixir.Unicode(50), unique=True)
    description = _elixir.Field(_elixir.UnicodeText)

    @classmethod
    def from_xml(cls, element):
        result = cls.get_by(name=element.get('name'))
        if not result:
            result = cls()
            result.from_dict(element.attrib)
        return result

class Parameter(_elixir.Entity):
    _elixir.using_options(tablename='parameter')

    # NOTE This is probably the most compilcated snippet of elixir code.
    label = _elixir.ManyToOne('ParameterLabel', column_kwargs=dict(index=True))
    parameter_set = _elixir.ManyToOne('ParameterSet',
                                      column_kwargs=dict(index=True))
    _elixir.using_table_options(_elixir.sqlalchemy.UniqueConstraint(
        'label_id', 'parameter_set_id'))

    value = _elixir.Field(_elixir.Float)

class ParameterSetGroup(_elixir.Entity):
    _elixir.using_options(tablename='parameter_set_group')

    name = _elixir.Field(_elixir.Unicode(50))
    description = _elixir.Field(_elixir.UnicodeText)

    simulation = _elixir.ManyToOne('Simulation')
    parameter_sets = _elixir.OneToMany('ParameterSet')

class ParameterSet(_elixir.Entity):
    _elixir.using_options(tablename='parameter_set')

    name = _elixir.Field(_elixir.Unicode(50))

    parameter_set_group = _elixir.ManyToOne('ParameterSetGroup')
    results = _elixir.OneToMany('SimulationResult')

    parameters = _elixir.OneToMany('Parameter')


class ParameterMapping(_elixir.Entity):
    _elixir.using_options(tablename='parameter_mapping')

    binding = _elixir.ManyToOne('Binding')
    parameter_label = _elixir.ManyToOne('ParameterLabel')
    local_name  = _elixir.Field(_elixir.Unicode(50))

    @classmethod
    def from_xml(cls, element):
        pl = ParameterLabel.query.get_by(name=element.get('parameter_label_name'))
        return cls(parameter_label=pl, local_name=element.get('local_name'))
