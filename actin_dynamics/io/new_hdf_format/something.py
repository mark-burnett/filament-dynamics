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

from . import hdf_format as _hdf_format
from . import utils as _utils

class Measurement(object):
    def __init__(self, table=None):
        self.table = table

    @classmethod
    def from_name(cls, hdf_file=None, parent_group=None, name=None):
        # XXX try/except here?
        table = self.hdf_file.createTable(group, name, _hdf_format.Measurement)
        return cls(table)

    def read(self):
        return _utils.table_as_list(self.table)

    def write(self, data):
        row = self.table.row
        for time, value in data:
            row['time']  = time
            row['value'] = value
            row.append()

        self.table.flush()

class MeasurementCollection(object):
    def __init__(self, hdf_file=None, group=None):
        self.hdf_file = hdf_file
        self.group    = group

    def read(self):
        pass

    def write(self, measurements):
        for name, data in measurements.iteritems():
            m = Measurement.from_name(hdf_file=self.hdf_file,
                                      parent_group=self.group,
                                      name=name)
            m.write(data)
