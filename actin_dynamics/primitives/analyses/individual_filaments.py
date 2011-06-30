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

from . import base_classes as _base_classes

from actin_dynamics import logger as _logger
_log = _logger.getLogger(__file__)

class IndividualFilament(_base_classes.Analysis):
    def __init__(self, sample_period=None, measurement_name=None,
                 simulation_index=None, filament_index=None,
                 label=None, **kwargs):
        self.sample_period = float(sample_period)
        self.measurement_name = measurement_name
        self.simulation_index = int(simulation_index)
        self.filament_index   = int(filament_index)
        _base_classes.Analysis.__init__(self, label=label, **kwargs)

    def perform(self, simulation_results, result_factory):
        times, values = simulation_results[self.simulation_index][
                'filaments'][self.filament_index]['measurements'][
                        self.measurement_name]
        errors = [0 for t in times]
        measurement = times, values, errors
        return result_factory(measurement, label=self.label)
