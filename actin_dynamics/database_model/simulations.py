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

class Simulation(_elixir.Entity):
    _elixir.using_options(tablename='simulation')

    name = _elixir.Field(_elixir.Unicode(50), unique=True)
    description = _elixir.Field(_elixir.UnicodeText)
    creation_date = _elixir.Field(_elixir.DateTime)

    # NOTE This is really one to one ish
    strand_factory = _elixir.ManyToOne('StrandFactory')

    transitions = _elixir.OneToMany('Transition')
    concentrations = _elixir.OneToMany('Concentration')
    end_conditions = _elixir.OneToMany('EndCondition')
    explicit_measurements = _elixir.OneToMany('ExplicitMeasurement')

    parameter_set_groups = _elixir.OneToMany('ParameterSetGroup')

class SimulationResult(_elixir.Entity):
    _elixir.using_options(tablename='simulation_result')

    parameter_set = _elixir.ManyToOne('ParameterSet')

    timestamp = _elixir.Field(_elixir.DateTime)
    revision = _elixir.Field(_elixir.Integer)

    measurement_data = _elixir.OneToMany('MeasurementData')
