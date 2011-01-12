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

import cPickle
import gzip

def write_object(data, filename):
    with open(filename, mode='wb') as f:
        compressor = gzip.GzipFile(fileobj=f)
        cPickle.dump(data, compressor, protocol=cPickle.HIGHEST_PROTOCOL)
        compressor.close()

def read_object(filename):
    with open(filename) as f:
        compressor = gzip.GzipFile(fileobj=f)
        return cPickle.load(compressor)

def combine_list_files(filenames):
    result = []
    for filename in filenames:
        result.extend(io.compressed.read_object(filename))
    return result
