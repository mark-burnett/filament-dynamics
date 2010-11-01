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

from .io import hdf
from .simulations import run_simulation

def run_simulations(simulation_factory, output_file_name):

    hdf_writer = hdf.Writer(output_file_name)
    pool = multiprocessing.Pool()

    try:
        for sim in simulation_factory:
            pool.apply_async(run_simulation, (sim,),
                             callback=hdf_writer.write_result)

        pool.close()
        pool.join()
    except KeyboardInterrupt:
        # Handle CTRL-C
        pool.terminate()
        raise

def sp_run_simulations(simulation_factory, output_file_name):
    hdf_writer = hdf.Writer(output_file_name)

    for sim in simulation_factory:
        hdf_writer.write_result(run_simulation(sim))
