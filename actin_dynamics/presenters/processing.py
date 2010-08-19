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
import datetime

import elixir

from actin_dynamics import database_model as dbm

from actin_dynamics.simulation.factories.simulations import make_simulation

def run_simulation(sim_id, par_set_id, code_revision, num_runs, pool):
    pool.imap_unordered(_process_simulation,
                        itertools.repeat((sim_id, par_set_id, code_revision), num_runs))

def _process_simulation(ids):
    # This is one try block, because any failure should cancel the process.
    try:
        sim_id, par_set_id, code_revision = ids
        simulation = dbm.Simulation.query.get(sim_id)
        parameter_set = dbm.ParameterSet.query.get(par_set_id)

        sim_object = make_simulation(simulation, parameter_set)

        final_strand, raw_measurements = sim_object.run()
        _convert_and_store_measurements(par_set_id, raw_measurements,
                                        code_revision)

    except Exception as e:
        # XXX log this exception stuff
        import traceback
        traceback.print_exc(e)

def _convert_and_store_measurements(par_set_id, raw_measurements,
                                    code_revision):
    converted_measurements = _convert_measurements(raw_measurements)
    _store_measurements(par_set_id, converted_measurements, code_revision)

def _convert_measurements(raw_measurements):
    converted_measurements = []
    for label, data in raw_measurements.iteritems():
        converted_measurements.append(_convert_single_measurement(label, data))
    return converted_measurements

def _convert_single_measurement(label, data):
    md = dbm.MeasurementData(measurement_label=label)
    for t, v in data:
        md.data.append(dbm.MeasurementDataEntry(time=t, value=v))
    return md

def _store_measurements(par_set_id, converted_measurements, code_revision):
    sr = dbm.SimulationResult(timestamp=datetime.datetime.now())
    sr.revision = code_revision
    for cm in converted_measurements:
        sr.measurement_data.append(cm)

    sr.parameter_set = dbm.ParameterSet.get(par_set_id)

    elixir.session.commit()
