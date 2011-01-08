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

from . import group_wrappers as _group_wrappers

# XXX this needs to become real...
def get_or_create_group(hdf_file, group_name, description=None):
    try:
        return hdf_file.getNode('/' + group_name)
    except:
        return hdf_file.createGroup('/', group_name, description)

def get_ps_ana(hdf_file):
    ps  = get_or_create_group(hdf_file, 'Simulations')
    ana = get_or_create_group(hdf_file, 'Analysis')
    return (_group_wrappers.MultipleParameterSetWrapper(ps),
            _group_wrappers.MultipleAnalysisWrapper(ana))

# XXX This doesn't seem like it belongs.
def unpack_measurement(measurement, shift=0, scaling=1):
    times, unscaled_values = zip(*measurement.read())
    scaled_values = [(v + shift) * scaling for v in unscaled_values]
    return times, scaled_values
