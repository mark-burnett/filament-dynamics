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

import pylab

from actin_dynamics import io

from . import utils

def full_run(hdf_file=None, parameter_set_number=None, parameter_labels=[],
             fluorescence_filename='pollard_length.dat',
             adppi_filename='pollard_cleavage.dat'):
    # Load the data.
    fluor_measurement = io.data.load_data(fluorescence_filename)
    adppi_data = io.data.load_data(adppi_filename)

    utils.plot_scatter_measurement(adppi_data)
    pylab.show()
