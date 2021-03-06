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

from actin_dynamics import logger
log = logger.getLogger(__file__)

from base_classes import EndCondition as _EndCondition

class Threshold(_EndCondition):
    def __init__(self, label=None, concentration_name=None, value=None,
            subtract_fraction=0, scaled_by=1):
        self.concentration_name = concentration_name
        self.value = float(value) * float(scaled_by) * (
                1 - float(subtract_fraction))

        _EndCondition.__init__(self, label=label)

    def reset(self):
        pass

    def __call__(self, time, filaments, concentrations):
        return concentrations[self.concentration_name].value > self.value

class FilamentMeasurementDecreasing(_EndCondition):
    def __init__(self, measurement_name=None, decreased_by=0.1, label=None):
        self.measurement_name = measurement_name
        self.decreased_by = float(decreased_by)
        self.peak_value = 0
        self.threshold = 0

        _EndCondition.__init__(self, label=label)

    def reset(self):
        pass

    def __call__(self, time, filaments, concentrations):
        current_value = 0
        for filament in filaments:
            current_value += filament['measurements'][self.measurement_name]
        if current_value > self.peak_value:
            self.peak_value = current_value
            self.threshold = current_value * (1 - self.decreased_by)
        elif current_value < self.threshold:
            return True
        return False
