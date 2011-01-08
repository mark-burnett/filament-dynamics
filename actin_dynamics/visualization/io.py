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

class GnuplotDialect(csv.Dialect):
    delimiter = ' '
    quotechar = '"'
    doublequote = True
    skipinitialspace = True
    lineterminator = '\n'
    quoting = csv.QUOTE_NONNUMERIC

def write_measurements(file_object, measurements):
    writer = csv.writer(file_object, dialect=GnuplotDialect)
    rows = _combine_measurements(measurements)
    writer.writerows(rows)

def _combine_measurements(measurements):
    times = measurements[0][0]

    results = []
    for i, t in enumerate(times):
        row = [t]
        for mt, ma, ml, mu in measurements:
            row.extend([ma[i], ml[i], mu[i]])
        results.append(row)

    return results
