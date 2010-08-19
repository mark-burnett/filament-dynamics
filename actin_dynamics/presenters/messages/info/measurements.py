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

import operator

class MeasurementList(object):
    def __init__(self, measurements):
        self.data = measurements

    @classmethod
    def from_simulation(cls, simulation):
        result = []
        for t in simulation.transitions:
            result.append((t.measurement_label.id, t.measurement_label.name))

        for c in simulation.concentrations:
            result.append((c.measurement_label.id, c.measurement_label.name))

        for em in simulation.explicit_measurements:
            result.append((em.measurement_label.id, em.measurement_label.name))

        result.sort(key=operator.itemgetter(1))

        return cls(result)
