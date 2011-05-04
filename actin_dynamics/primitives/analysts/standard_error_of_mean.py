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

import math
import operator

from .base_classes import Analyst

from actin_dynamics import database

from . import analyst_utils

from actin_dynamics.numerical import workalike, measurements

from actin_dynamics import logger
log = logger.getLogger(__file__)

class StandardErrorMean(Analyst):
    def __init__(self, source_name=None, source_type=None, #'observation',
                 scale_by=1, add=0, subtract=0, *args, **kwargs):
        self.source_name = source_name
        self.source_type = source_type

        self.scale_by = scale_by
        self.add      = add
        self.subtract = subtract

        Analyst.__init__(self, *args, **kwargs)

    def analyze(self, observations, analyses):
        source = _choose_source(observations, analyses, self.source_type)
        raw_data = source[self.source_name]

        times, collated_data = analyst_utils.collate_data(raw_data)

        # XXX Create real measurement type? - maybe not right now
        values, errors = _sem(collated_data, scale_by=self.scale_by,
                              add=self.add - self.subtract)

        return database.Analysis(value=(times, values, errors))


def _choose_source(observations, analyses, source_type):
    if 'observation' == source_type.lower():
        source = observations
    elif 'analyses' == source_type.lower():
        source = analyses
    else:
        raise RuntimeError('Unknown source type %r.' % source_type)
    return source


def _sem(collated_data, scale_by=1, add=0):
    means = []
    errors = []
    for values in collated_data:
        length = len(values)
        sqrt_N = math.sqrt(length)

        adjusted_values = [float(v) * scale_by for v in values]
        mean = sum(adjusted_values) / length
        error = workalike.std(adjusted_values, mean) / sqrt_N
        means.append(mean + add)
        errors.append(error)
    return means, errors
