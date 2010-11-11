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

class TableWrapper(object):
    def __init__(self, table=None):
        self.table = table

    @classmethod
    def in_group(cls, hdf_file=None, parent_group=None, name=None):
        table = hdf_file.createTable(parent_group, name, self.description)
        return cls(table)

    def read(self):
        return self.table.read()

    def write(self, data):
        row = self.table.row
        column_names = data.colnams
        for d in data:
            for name, value in itertools.izip(column_names, d):
                row[name] = value
            row.append()

        self.table.flush()

class DictionaryTable(TableWrapper):
    def read(self):
        return dict(self.table.read())

    def write(self, data):
        row = self.table.row
        for k, v in data.iteritems():
            row[self.key]  = k
            row[self.value] = v
            row.append()

        self.table.flush()

class SingleValueTable(TableWrapper):
    def read(self):
        return [row[0] for row in self.table.read()]

    def write(self, data):
        row = self.table.row
        for v in data:
            row[self.column_name] = v
            row.append()

        self.table.flush()

class Collection(object):
    def __init__(self, hdf_file=None, group=None):
        self.hdf_file = hdf_file
        self.group    = group

    @classmethod
    def in_group(cls, hdf_file=None, parent_group=None, name=None):
        group = hdf_file.createGroup(parent_group, name)
        return cls(hdf_file=hdf_file, group=group)

    def read(self):
        result = {}
        for child in self.group:
            m = self.description(child)
            result[child._v_name] = m.read()
        return result

    def write(self, children):
        for name, data in children.iteritems():
            c = self.child_wrapper.in_group(hdf_file=self.hdf_file,
                                            parent_group=self.group,
                                            name=name)
            c.write(data)
