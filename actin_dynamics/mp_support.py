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

import tables

from .io import hdf
from .simulations import run_simulation

_compession_filter = tables.Filters(complevel=9)

def run_simulations(simulation_factory, output_file_name):
    with tables.openFile(output_file_name, mode='w',
                         filters=_compession_filter) as output_file:
        hdf_writer = hdf.SimulationWriter(output_file)
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
    with tables.openFile(output_file_name, mode='w',
                         filters=_compession_filter) as output_file:
        hdf_writer = hdf.SimulationWriter(output_file)

        for sim in simulation_factory:
            hdf_writer.write_result(run_simulation(sim))
