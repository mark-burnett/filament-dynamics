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

import csv

class DataThiefDialect(csv.Dialect):
    delimiter = ' '
    quotechar = '"'
    doublequote = True
    skipinitialspace = True
    lineterminator = '\r\n'
    quoting = csv.QUOTE_NONNUMERIC

def load_data(filename):
    results = []
    with open(filename) as f:
        reader = csv.reader(f, dialect=DataThiefDialect)
        for row in reader:
            if 0 != len(row) and '#' != row[0]:
                new_row = map(float, row)
                results.append(new_row)
    return zip(*results)
