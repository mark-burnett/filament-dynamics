#    Copyright (C) 2011 Mark Burnett
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

import csv
import numpy

import scipy.stats

from actin_dynamics import database
from actin_dynamics.io import data

from actin_dynamics.numerical import interpolation as _interpolation

def _get_qof(session, alpha):
    vals = [r.get_objective('length_fit') for r in session.experiments[0].runs]
    vals = filter(None, vals)

    chi2 = numpy.mean(vals)
    std_err = numpy.std(vals, ddof=1)

    t = scipy.stats.t.ppf(1 - alpha/2, len(vals) - 1)

    ci = t * std_err

    return chi2, chi2 - ci, chi2 + ci, ci / chi2 * 100

def _get_dumb_qof(session, alpha):
    vals = [r.get_objective('length_fit') for r in session.experiments[0].runs]
    vals = filter(None, vals)
    chi2 = numpy.mean(vals)

    return chi2, 0, 0, 0


def save_qof(session_ids, alpha=0.01,
        cooperative_filename='results/depoly_cooperative_qof.dat',
        vectorial_filename='results/depoly_vectorial_qof.dat'):
    dbs = database.DBSession()
    coop_results = []
    vec_results = None
    for sid in session_ids:
        session = dbs.query(database.Session).get(sid)

        chi2, chi2_min, chi2_max, chi2_pct = _get_qof(session, alpha)
#        chi2, chi2_min, chi2_max, chi2_pct = _get_dumb_qof(session, alpha)

        cooperativity = session.parameters.get('release_cooperativity')
        if cooperativity is not None:
            coop_results.append(
                    [cooperativity, chi2, chi2_min, chi2_max, chi2_pct])
        else:
            vec_results = [chi2, chi2_min, chi2_max, chi2_pct]

    if coop_results:
        coop_results.sort()
        _small_writer(cooperative_filename, coop_results,
                ['Cooperativity', 'Chi^2', 'Min CI', 'Max CI', '% Error'],
                header="# Cooperative quality of fit for Jegou 2011\n")

    if vec_results:
        _small_writer(vectorial_filename, [vec_results],
                ['Chi^2', 'Min CI', 'Max CI', '% Error'],
                header="# Vectorial quality of fit for Jegou 2011\n")


def save_means(barbed_sid, jegou_sid, cooperative_sid):
    save_mean(barbed_sid,
            'results/depoly_mean_barbed.dat')
    save_mean(jegou_sid,
            'results/depoly_mean_jegou.dat')
    save_mean(cooperative_sid,
            'results/depoly_mean_cooperative.dat')

def save_mean(sid, filename):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(sid)
    e = session.experiments[0]

    polymerization_duration = e.all_parameters['polymerization_duration']
    simulation_duration = e.all_parameters['simulation_duration']
    sample_period = e.all_parameters['sample_period']
    times = numpy.arange(0, simulation_duration - polymerization_duration
            + float(sample_period)/2, sample_period)
    values = _get_timecourse(e.runs[0], times, polymerization_duration)

    rows = zip(times, values)
    _small_writer(filename, rows, ['times', 'mean_filament_length'])
    

def save_timecourses(random_sid, vectorial_sid, barbed_sid, jegou_sid,
        cooperative_sid):
    save(random_sid, 'results/depoly_tc_random.dat')
    save(vectorial_sid, 'results/depoly_tc_vectorial.dat')

    save(barbed_sid, 'results/depoly_tc_barbed.dat')

    save(jegou_sid, 'results/depoly_tc_jegou.dat')

    save(cooperative_sid, 'results/depoly_tc_cooperative.dat')


def save(session_id,
        output_filename='results/depolymerization_timecourses.dat'):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)
    e = session.experiments[0]

    polymerization_duration = e.all_parameters['polymerization_duration']
    simulation_duration = e.all_parameters['simulation_duration']
    sample_period = e.all_parameters['sample_period']
    
    times = numpy.arange(0, simulation_duration - polymerization_duration
            + float(sample_period)/2, sample_period)
    values = []
    for run in session.experiments[0].runs:
        values.append(_get_timecourse(run, times, polymerization_duration))

    tv = numpy.transpose(values)
    results = numpy.vstack((times, values))
    results = numpy.transpose(results)

    _small_writer(output_filename, results, ['times', 'filament_length'])

def _get_timecourse(run, resample_times, poly_duration):
    # Grab the analysis
    times, values, errors = run.analyses['length']

    times = numpy.array(times)
    values = numpy.array(values)

    times -= poly_duration

    # resample
    sampled_values = numpy.array(_interpolation.resample_measurement(
        (times, values), resample_times)[1])

    numpy.putmask(sampled_values, sampled_values < 50, float('nan'))

    return sampled_values

def _small_writer(filename, results, names, header=None):
    with open(filename, 'w') as f:
        # Header lines, identifying x, y, column name
        f.write('# Auto-collated output:\n')
        if header:
            f.write(header)
        for i, name in enumerate(names):
            f.write('# Column %i: %s\n' % ((i + 1), name))
        # CSV dump of actual data
        w = csv.writer(f, dialect=data.DatDialect)
        w.writerows(results)
