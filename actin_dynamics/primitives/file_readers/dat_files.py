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

from os import path as _ospath
import csv as _csv

from .base_classes import FileReader as _FileReader

from actin_dynamics.numerical import interpolation as _interpolation
from actin_dynamics.numerical import workalike as _workalike
from actin_dynamics.io import comments as _comments

class _DatDialect(_csv.Dialect):
    delimiter = ' '
    quotechar = '"'
    doublequote = True
    skipinitialspace = True
    lineterminator = '\r\n'
    quoting = _csv.QUOTE_NONNUMERIC


class DatReader(_FileReader):
    def __init__(self, xmin=None, xmax=None, sample_period=None,
                 filename=None, base_directory='experimental_data',
                 interpolate_data=False, label=None):
        self.xmin = xmin
        self.xmax = xmax
        self.sample_period = sample_period
        self.interpolate_data = interpolate_data

        self.filename = filename
        self.base_directory = base_directory

        _FileReader.__init__(self, label=label)

    def run(self):
        full_filename = _ospath.join(self.base_directory, self.filename)
        f = _comments.CommentFilter.from_filename(full_filename)
        reader = _csv.reader(f, dialect=_DatDialect)

        results = []
        for row in reader:
            new_row = map(float, row)
            results.append(new_row)

        raw_results = zip(*results)
        if not self.interpolate_data:
            return raw_results

        sample_times = _workalike.arange(self.xmin, self.xmax,
                                         self.sample_period)
        return _interpolation.resample_measurement(raw_results, sample_times)
