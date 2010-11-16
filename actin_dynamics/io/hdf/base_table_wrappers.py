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

import itertools

class TableWrapper(object):
    def __init__(self, table=None):
        self.table = table

    def __str__(self):
        return str(self.table)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.table))

    @classmethod
    def in_group(cls, hdf_file=None, parent_group=None, name=None):
        table = hdf_file.createTable(parent_group, name, cls.description)
        return cls(table)

    @classmethod
    def create(cls, parent_group=None, name=None):
        hdf_file = parent_group._v_file
        table = hdf_file.createTable(parent_group, name, cls.description)
        return cls(table)

    def read(self):
        return self.table.read()

    def write(self, data):
        row = self.table.row
        for datum in data:
            for name, value in itertools.izip(self.table.colnames, datum):
                row[name] = value
            row.append()

        self.table.flush()

# XXX Needs to really use the getitem/setitem interface.
class DictionaryTable(TableWrapper):
    def __init__(self, table=None):
        TableWrapper.__init__(self, table)
        self.read()

    def read(self):
        self._dict = dict(self.table.read())
        return self._dict

    def write(self, data):
        row = self.table.row
        for k, v in data.iteritems():
            row[self.key]  = k
            row[self.value] = v
            row.append()

        self.table.flush()
        self.read() # update _dict

    def __getitem__(self, key):
        return self._dict[key]

class SingleValueTable(TableWrapper):
    def read(self):
        return [row[0] for row in self.table.read()]

    def write(self, data):
        row = self.table.row
        for v in data:
            row[self.column_name] = v
            row.append()

        self.table.flush()
