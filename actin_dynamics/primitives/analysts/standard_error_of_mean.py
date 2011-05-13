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

from .base_classes import Analyst

from actin_dynamics import database

from . import analyst_utils

from actin_dynamics.numerical import measurements, transform, sem, collate


class StandardErrorMean(Analyst):
    def __init__(self, source_name=None, source_type=None,
                 scale_by=None, add=0, subtract=0, *args, **kwargs):
        self.source_name = source_name
        self.source_type = source_type

        self.scale_by = scale_by
        self.add      = add
        self.subtract = subtract

        Analyst.__init__(self, *args, **kwargs)

    def analyze(self, observations, analyses):
        source = analyst_utils.choose_source(observations, analyses,
                self.source_type)
        raw_data = source[self.source_name]

        times, collated_data = collate.collate_on_times(raw_data)

        # XXX Create real measurement type? - maybe not right now
        values, errors = collated_standard_error_of_mean(
                collated_data, scale_by=self.scale_by,
                add=self.add - self.subtract)

        return database.Analysis(value=(times, values, errors))


class KeyedStandardErrorMean(Analyst):
    def __init__(self, source_name=None, source_type=None,
                 scale_by=None, add=0, subtract=0, *args, **kwargs):
        self.source_name = source_name
        self.source_type = source_type

        self.scale_by = scale_by
        self.add      = add
        self.subtract = subtract

        Analyst.__init__(self, *args, **kwargs)

    def analyze(self, observations, analyses):
        source = analyst_utils.choose_source(observations, analyses,
                self.source_type)
        keyed_data = transform.key_transform(source[self.source_name])
        results = {}
        for name, raw_data in keyed_data.iteritems():
            times, collated_data = collate.collate_on_times(raw_data)

            values, errors = collated_standard_error_of_mean(
                    collated_data, scale_by=self.scale_by,
                    add=self.add - self.subtract)
            results[name] = (times, values, errors)

        return database.Analysis(value=results)


def collated_standard_error_of_mean(collated_data, scale_by=None, add=0):
    '''
    Compute the standard error of the mean for collated data.
    '''
    means = []
    errors = []
    for values in collated_data:
        mean, error = sem.standard_error_of_mean(values,
                scale_by=scale_by, add=add)
        means.append(mean)
        errors.append(error)
    return means, errors
