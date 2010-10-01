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

class SimulationData(_elixir.Entity):
    _elixir.using_options(tablename='simulation_data')

    simulation_result = _elixir.ManyToOne('SimulationResult')
    measurement_label = _elixir.ManyToOne('MeasurementLabel')

    data = _elixir.OneToMany('SimulationDataEntry')

class SimulationDataEntry(_elixir.Entity):
    _elixir.using_options(tablename='simulation_data_entry')

    simulation_data = _elixir.ManyToOne('SimulationData')
    time = _elixir.Field(_elixir.Float)
    value = _elixir.Field(_elixir.Float)


class StrandData(_elixir.Entity):
    _elixir.using_options(tablename='strand_data')

    simulation_result = _elixir.ManyToOne('SimulationResult')
    measurement_label = _elixir.ManyToOne('MeasurementLabel')

    strands = _elixir.ManyToOne('StrandIdentifier')

class StrandIdentifier(_elixir.Entity):
    _elixir.using_options(tablename='strand_identifier')

    data = _elixir.ManyToOne('StrandDataEntry')

class StrandDataEntry(_elixir.Entity):
    _elixir.using_options(tablename='strand_data_entry')

    strand_identifier = _elixir.OneToMany('StrandIdentifier')

    time = _elixir.Field(_elixir.Float)
    value = _elixir.Field(_elixir.Float)
