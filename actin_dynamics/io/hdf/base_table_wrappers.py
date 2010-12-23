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

from . import base_wrappers as _base_wrappers 

class TableWrapper(_base_wrappers.Wrapper):
    def __init__(self, table=None):
        _base_wrappers.Wrapper.__init__(self, table)

    @classmethod
    def in_group(cls, hdf_file=None, parent_group=None, name=None):
        table = hdf_file.createTable(parent_group, name,
                                     description=cls.description,
                                     expectedrows=100)
        return cls(table)

    @classmethod
    def create(cls, parent_group=None, name=None):
        hdf_file = parent_group._v_file
        table = hdf_file.createTable(parent_group, name,
                                     description=cls.description,
                                     expectedrows=100)
        return cls(table)

    def read(self):
        return self._pytables_object.read()
    
    def __iter__(self):
        return iter(self.read())

    def write(self, data):
        row = self._pytables_object.row
        for datum in data:
            for name, value in itertools.izip(self._pytables_object.colnames,
                                              datum):
                row[name] = value
            row.append()

        self._pytables_object.flush()

    def __len__(self):
        return self._pytables_object.nrows

# XXX Needs to really use the getitem/setitem interface.
class DictionaryTable(TableWrapper):
    def __init__(self, table=None):
        TableWrapper.__init__(self, table)
        self.read()

    def read(self):
        self._dict = dict(self._pytables_object.read())
        return self._dict

    def write(self, data):
        row = self._pytables_object.row
        for k, v in data.iteritems():
            row[self.key]  = k
            row[self.value] = v
            row.append()

        self._pytables_object.flush()
        self.read() # update _dict

    def __getitem__(self, key):
        return self._dict[key]

class SingleValueTable(TableWrapper):
    def read(self):
        return [row[0] for row in self._pytables_object.read()]

    def write(self, data):
        row = self._pytables_object.row
        for v in data:
            row[self.column_name] = v
            row.append()

        self._pytables_object.flush()
