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

import multiprocessing

from . import io as _io
from . import simulations as _simulations

def run_simulations(simulation_factory, output_file_name):
    pool = multiprocessing.Pool()

    try:
        results = []
        for parameter_set, ssg in simulation_factory:
            ps_result = pool.map(_simulations.run_and_report_sim, ssg)
            # Must pass a timeout or keyboard interrupt fails
#            ps_result.get(999999)
            results.append({'parameters':  parameter_set,
                            'simulations': ps_result})

        pool.close()
        pool.join()

    except KeyboardInterrupt:
        # Handle CTRL-C
        pool.terminate()
        raise
    
    _io.compressed.write_object(results, output_file_name)

def sp_run_simulations(simulation_factory, output_file_name):
    results = []
    for parameter_set in simulation_factory:
        ps_result = map(_simulations.run_simulation, simulation_factory)
        results.append({'parameters': parameter_set, 'simulations': ps_result})

    _io.write_simulation_data(results, output_file_name)
