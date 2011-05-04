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

from .base_classes import Analyst

from actin_dynamics import database
from actin_dynamics.numerical import measurements

class SumAnalyses(Analyst):
    def __init__(self, label=None, **weights):
        self.weights = weights
        Analyst.__init__(self, label=label)

    def analyze(self, observations, analyses):
        weighted_measurements = []
        for name, weight in self.weights.iteritems():
            weighted_measurements.append(
                    measurements.scale(analyses[name].value, weight))
        result = measurements.add(weighted_measurements)
        return database.Analysis(value=result)
