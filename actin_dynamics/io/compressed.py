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
    f = open(filename, mode='wb')
    compressor = gzip.GzipFile(fileobj=f)
    cPickle.dump(data, compressor, protocol=cPickle.HIGHEST_PROTOCOL)
    compressor.close()

def read_object(filename):
    f = open(filename)
    compressor = gzip.GzipFile(fileobj=f)
    return cPickle.load(compressor)

def read_objects(filename):
    f = open(filename)
    compressor = gzip.GzipFile(fileobj=f)
    results = []
    try:
        while compressor:
            results.append(cPickle.load(compressor))
    except EOFError:
        pass
    f.close()
    return results

def output_stream(filename):
    f = open(filename, mode='wb')
    compressor = gzip.GzipFile(fileobj=f)
    return compressor


def combine_files(filenames):
    results = []
    for filename in filenames:
        results.extend(read_objects(filename))
    return results
