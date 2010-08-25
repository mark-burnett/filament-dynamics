#    Copyright (C) 2010 Mark Burnett
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

from .simulations import Simulation as _Simulation

from .parameters import Parameter as _Parameter

class ParameterSetGroup(_elixir.Entity):
    _elixir.using_options(tablename='parameter_set_group')

    name = _elixir.Field(_elixir.Unicode(50))
    description = _elixir.Field(_elixir.UnicodeText)

    simulation = _elixir.ManyToOne('Simulation')
    parameter_sets = _elixir.OneToMany('ParameterSet')

    @classmethod
    def from_xml(cls, element):
        sim = _Simulation.get_by(name=element.get('simulation_name'))

        result = cls.get_by(name=element.get('name'), simulation=sim)
        if not result:
            result = cls(name=element.get('name'),
                         description=element.get('name'),
                         simulation=sim)

        for ps_xml in element:
            result.parameter_sets.append(
                    ParameterSet.from_xml(ps_xml))

        return result

class ParameterSet(_elixir.Entity):
    _elixir.using_options(tablename='parameter_set')

    name = _elixir.Field(_elixir.Unicode(50))
    description = _elixir.Field(_elixir.UnicodeText)

    parameter_set_group = _elixir.ManyToOne('ParameterSetGroup')
    results = _elixir.OneToMany('SimulationResult')

    parameters = _elixir.OneToMany('Parameter')

    @classmethod
    def from_xml(cls, element):
        result = cls(name=element.get('name'))
        for p_xml in element:
            result.parameters.append(_Parameter.from_xml(p_xml))

        return result
