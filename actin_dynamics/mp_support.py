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
import multiprocessing

from . import analysis as _analysis
from . import io as _io
from . import simulations as _simulations

def run_simulations(simulation_factory, output_file_name):
    pool = multiprocessing.Pool()

    try:
        results = []
        for parameters, ssg in simulation_factory:
            ps_result = pool.map_async(_simulations.run_and_report, ssg)
            sim_ps = {'parameters': parameters,
                      'simulations': ps_result.get(999999)}
            ana_ps = _analysis.perform_common_single(sim_ps)
            results.append(ana_ps)

        pool.close()
        pool.join()

    except KeyboardInterrupt:
        # Handle CTRL-C
        pool.terminate()
        print 'Keyboard Interrupt received.  Writing current reults.'
    
    _io.compressed.write_object(results, output_file_name)

def sp_run_simulations(simulation_factory, output_file_name):
    results = []
    for parameter_set, ssg in simulation_factory:
        ps_result = map(_simulations.run_report_and_analyze, ssg)
        sim_ps = {'parameters': parameters,
                  'simulations': ps_result.get(999999)}
        ana_ps = _analysis.perform_common_single(sim_ps)
        results.append(ana_ps)

    _io.compressed.write_object(results, output_file_name)
