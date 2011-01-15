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

import cPickle as _cPickle

from . import io as _io
from . import simulations as _simulations

from .analysis import perform_common_single as _perform_common_single

def run_simulations(simulation_factory, output_file_name):
    output_stream = _io.compressed.output_stream(output_file_name)
    for parameter_set, ssg in simulation_factory:
        ps_result = map(_simulations.run_and_report, ssg)

        full_set = {'parameters': parameter_set, 'simulations': ps_result}

        _cPickle.dump(_perform_common_single(full_set), output_stream,
                      protocol=cPickle.HIGHEST_PROTOCOL)

    output_stream.close()
