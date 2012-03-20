#    Copyright (C) 2012 Mark Burnett
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

import operator
import numpy
import scipy
import scipy.optimize
import scipy.stats

import scikits.statsmodels.api as sm

from actin_dynamics.io import data
from actin_dynamics import database


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


def save_xy(session_id, output_filename='rtest.dat'):
    x, y = get_xy(session_id)
    _small_writer(output_filename, zip(x,y), [])


def get_xy(session_id, target='pi_fit', parameter='release_rate'):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)
    runs = session.experiments[0].runs

    pairs = sorted([(r.get_objective(target), r.parameters[parameter])
            for r in runs if r.get_objective(target) is not None],
            key = operator.itemgetter(1))

    y_values, x_values = zip(*pairs)
    x_values = numpy.array(x_values)
    y_values = numpy.array(y_values)

    return x_values, y_values

def get_parameter(session_id, parameter_name):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)
    runs = session.experiments[0].runs
    return runs[0].all_parameters.get(parameter_name, None)


def fit_xy(x_values, y_values, alpha):
    guess_coeffs = scipy.polyfit(x_values, y_values, 2)

    # Calculate good starting parameter guesses for curve_fit
    guess_r = - guess_coeffs[1] / (2 * guess_coeffs[0])
    guess_k = guess_coeffs[0]
    guess_c = float(scipy.polyval(guess_coeffs, guess_r))

    def f(x, r, k, c):
        return k * (x - r)**2 + c

    cf_pars, cf_cov = scipy.optimize.curve_fit(f, x_values, y_values,
            (guess_r, guess_k, guess_c))

    rate = cf_pars[0]
    k = cf_pars[1]
    c = cf_pars[2]

    t = scipy.stats.t.ppf(1 - alpha/2, len(x_values) - 3)

    rate_std_err = numpy.sqrt(cf_cov[0,0])
    min_rate = rate - rate_std_err * t
    max_rate = rate + rate_std_err * t
    rate_pct_error =  100 * t * rate_std_err / rate
    rate_pack = (rate, min_rate, max_rate, rate_pct_error)

    k_std_err = numpy.sqrt(cf_cov[1,1])
    min_k = k - k_std_err * t
    max_k = k + k_std_err * t
    k_pct_error =  100 * t * k_std_err / k
    k_pack = (k, min_k, max_k, k_pct_error)

    c_std_err = numpy.sqrt(cf_cov[2,2])
    min_c = c - c_std_err * t
    max_c = c + c_std_err * t
    c_pct_error =  100 * t * c_std_err / c
    c_pack = (c, min_c, max_c, c_pct_error)

    return rate_pack, k_pack, c_pack


def direct_fit(session_id, alpha):
    x_values, y_values = get_xy(session_id)

    rate_pack, k_pack, c_pack = fit_xy(x_values, y_values, alpha)

    rate, min_rate, max_rate, rate_pct_error = rate_pack
    c, min_c, max_c, c_pct_error = c_pack

    cooperativity = get_parameter(session_id, 'release_cooperativity')

    return cooperativity, rate, min_rate, max_rate, rate_pct_error, c, min_c, max_c, c_pct_error


def plot_session(session_id, alpha=0.01):
    x_values, y_values = get_xy(session_id)
    guess_coeffs = scipy.polyfit(x_values, y_values, 2)

    # Calculate good starting parameter guesses for curve_fit
    guess_r = - guess_coeffs[1] / (2 * guess_coeffs[0])
    guess_k = guess_coeffs[0]
    guess_c = float(scipy.polyval(guess_coeffs, guess_r))

    def f(x, r, k, c):
        return k * (x - r)**2 + c

    cf_pars, cf_cov = scipy.optimize.curve_fit(f, x_values, y_values,
            (guess_r, guess_k, guess_c))

    rate = cf_pars[0]
    c = cf_pars[2]

    rate_std_err = numpy.sqrt(cf_cov[0,0])
    c_std_err = numpy.sqrt(cf_cov[2,2])
    t = scipy.stats.t.ppf(1 - alpha/2, len(x_values) - 3)

    min_rate = rate - rate_std_err * t
    max_rate = rate + rate_std_err * t
    rate_pct_error =  100 * t * rate_std_err / rate

    min_c = c - c_std_err * t
    max_c = c + c_std_err * t
    c_pct_error =  100 * t * c_std_err / c

    cooperativity = get_parameter(session_id, 'release_cooperativity')

    import bisect
    xi = bisect.bisect(x_values, rate)

    near_x = x_values[xi]

    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)
    runs = session.experiments[0].runs

    the_run = None
    for run in runs:
        if near_x == run.parameters['release_rate']:
            the_run = run
            break

    import pylab

    pylab.subplot(2,1,1)
    plotx = numpy.linspace(x_values[0], x_values[-1], 500)
    pylab.plot(x_values, y_values, 'ro')
    pylab.plot(plotx, f(plotx, *cf_pars), 'b-')
    
    pylab.subplot(2,1,2)
    pi_x, pi_y, pi_e = the_run.analyses['Pi']
    pylab.plot(pi_x, pi_y, 'r-')

    p_data = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/phosphate_concentration.dat')
    d_t, d_p = p_data
    pylab.plot(d_t, d_p, 'k-')




def save_fits(cooperative_ids, vectorial_id, alpha=0.01,
        cooperative_filename='results/melki_cooperative_fit.dat',
        vectorial_filename='results/melki_vectorial_fit.dat'):
    coop_results = []
    for cid in cooperative_ids:
        try:
            coop_results.append(direct_fit(cid, alpha=alpha))
        except ValueError:
            pass
    coop_results.sort()
    _small_writer(cooperative_filename, coop_results,
            ['Cooperativity', 'Rate', 'Min Rate', 'Max Rate', 'Rate % Error',
                'Chi^2', 'Min Chi^2', 'Max Chi^2', 'Chi^2 % Error'],
            header='# Fit of cooperative models to Melki data\n# alpha = %s' % alpha)

    try:
        vec_results = [direct_fit(vectorial_id, alpha=alpha)[1:]]
        _small_writer(vectorial_filename, vec_results,
                ['Rate', 'Min Rate', 'Max Rate', 'Rate % Error',
                    'Chi^2', 'Min Chi^2', 'Max Chi^2', 'Chi^2 % Error'],
                header='# Fit of vectorial model to Melki data\n# alpha = %s' % alpha)
    except ValueError:
        pass

def fnc_plot(session_id, x_range=0.1, alpha=0.01, 
        num_parabola_points=500, interactive=True, output_filename=None):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)

    x, y = get_xy(session_id, target='f_fit', parameter='filament_tip_concentration')

#    min_x = x[0]
#    max_x = x[-1]
#    filtered_x = x
#    filtered_y = y

    imin = numpy.argmin(y)
    xmin = x[imin]
    min_x = (1-x_range) * xmin
    max_x = (1+x_range) * xmin
    indices = numpy.intersect1d(numpy.argwhere( min_x < x),
            numpy.argwhere(max_x > x))
    filtered_x = x.take(indices)
    filtered_y = y.take(indices)

    rate_pack, k_pack, c_pack = fit_xy(filtered_x, filtered_y, alpha)

    def f(x, r, k, c):
        return k * (x - r)**2 + c
    par_x_vals = numpy.linspace(min_x, max_x, num_parabola_points)
    par_y_vals = f(par_x_vals, rate_pack[0], k_pack[0], c_pack[0])

    from . import plot_util

    f = plot_util.figure(interactive=interactive)
    top_axes = f.add_subplot(2, 1, 1)
    top_axes.plot(x, y, 'r.')
    top_axes.set_xlabel(r'Filament Number Concentration [$\mu$M]')
    top_axes.set_ylabel('Chi^2 Fit to Melki Data')
    top_axes.axvline(rate_pack[0], 0, 1, color='g', linestyle=':')
#    top_axes.set_yscale('log')
    top_axes.xaxis.major.formatter.set_powerlimits((0,0))
#    top_axes.set_xlim(0, x[-1])

    bot_axes = f.add_subplot(2, 1, 2)
    bot_axes.plot(filtered_x, filtered_y, 'ro')
    bot_axes.plot(par_x_vals, par_y_vals, 'b-')
    bot_axes.set_xlabel(r'Filament Number Concentration [$\mu$M]')
    bot_axes.set_ylabel('Chi^2 Fit to Melki Data')
    bot_axes.axvline(rate_pack[0], 0, 1, color='g', linestyle='-')
    bot_axes.axvline(rate_pack[1], 0, 1, color='g', linestyle=':')
    bot_axes.axvline(rate_pack[2], 0, 1, color='g', linestyle=':')
    bot_axes.xaxis.major.formatter.set_powerlimits((0,0))
    bot_axes.set_xlim(min_x, max_x)

    top_axes.set_title(r'FNC = %.3e $\mu$M +/- %.3f%%' % (
            rate_pack[0], rate_pack[-1]))


def plot_fit(session_id, x_range=0.1, alpha=0.01,
        num_parabola_points=500, interactive=True, output_filename=None):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)
    cooperativity = session.parameters.get('release_cooperativity', None)

    x, y = get_xy(session_id)

    min_x = x[0]
    max_x = x[-1]
    filtered_x = x
    filtered_y = y

#    imin = numpy.argmin(y)
#    xmin = x[imin]
#    min_x = (1-x_range) * xmin
#    max_x = (1+x_range) * xmin
#    indices = numpy.intersect1d(numpy.argwhere( min_x < x),
#            numpy.argwhere(max_x > x))
#    filtered_x = x.take(indices)
#    filtered_y = y.take(indices)

    rate_pack, k_pack, c_pack = fit_xy(filtered_x, filtered_y, alpha)

    def f(x, r, k, c):
        return k * (x - r)**2 + c
    par_x_vals = numpy.linspace(min_x, max_x, num_parabola_points)
    par_y_vals = f(par_x_vals, rate_pack[0], k_pack[0], c_pack[0])

    from . import plot_util

    f = plot_util.figure(interactive=interactive)
#    top_axes = f.add_subplot(2, 1, 1)
#    top_axes.plot(x, y, 'r.')
#    top_axes.set_xlabel('Release Rate [s^-1]')
#    top_axes.set_ylabel('Chi^2 Fit to Melki Data')
#    top_axes.axvline(rate_pack[0], 0, 1, color='g', linestyle=':')
#    top_axes.set_yscale('log')
#    top_axes.xaxis.major.formatter.set_powerlimits((0,0))
#    top_axes.set_xlim(0, x[-1])

    bot_axes = f.add_subplot(1, 1, 1)
    bot_axes.plot(filtered_x, filtered_y, 'ro')
    bot_axes.plot(par_x_vals, par_y_vals, 'b-')
    bot_axes.set_xlabel('Release Rate [s^-1]')
    bot_axes.set_ylabel('Chi^2 Fit to Melki Data')
    bot_axes.axvline(rate_pack[0], 0, 1, color='g', linestyle='-')
    bot_axes.axvline(rate_pack[1], 0, 1, color='g', linestyle=':')
    bot_axes.axvline(rate_pack[2], 0, 1, color='g', linestyle=':')
    bot_axes.xaxis.major.formatter.set_powerlimits((0,0))
    bot_axes.set_xlim(min_x, max_x)

    if cooperativity:
        bot_axes.set_title(r'$\rho_d$ = %.0e, rate = %.3e +/- %.3f%%' % (
                cooperativity, rate_pack[0], rate_pack[-1]))
    else:
        bot_axes.set_title(r'Vectorial, rate = %.3e +/- %.3f%%' % (
                rate_pack[0], rate_pack[-1]))

    if not interactive:
        if output_filename is None:
            output_filename = _make_filename(cooperativity)
        f.savefig(output_filename)

def plot_nearest_fit_timecourse(session_id, alpha=0.01):
    rates, chi2s = get_xy(session_id)
    rate_pack, k_pack, c_pack = fit_xy(rates, chi2s, alpha)

    import bisect
    xi = bisect.bisect(rates, rate_pack[0])
    nearest_rate = rates[xi]

    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)
    runs = session.experiments[0].runs
    nearest_run = None
    for run in runs:
        if run.parameters['release_rate'] == nearest_rate:
            nearest_run = run
            break;

    t, fact, p, fe, pe = _get_timecourses(nearest_run)

    f_data = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/factin_concentration.dat')
    p_data = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/phosphate_concentration.dat')
    import pylab
    f = pylab.figure()
    a = f.add_subplot(1, 1, 1)
    a.plot(f_data[0], f_data[1], 'k-', label='[F] Data')
    a.plot(p_data[0], p_data[1], 'k--', label='[Pi] Data')

    a.plot(t, fact, 'b-', label='[F] Sim')
    a.plot(t, p, 'b--', label='[Pi] Sim')

    a.set_ylim([0, 35])

def save_best_timecourses(session_ids, alpha=0.01,
        f_output_filename='results/melki_timecourses_f.dat',
        p_output_filename='results/melki_timecourses_p.dat'):
    tcs = [_get_best_tc(sid, alpha) for sid in session_ids]
    tcs.sort()
    
    flipped = zip(*tcs)
    cooperativities, traces = flipped[0], flipped[1:]

    labels = []
    for c in cooperativities:
        if c is not None:
            labels.append('%.0e' % c)
        else:
            labels.append('Vectorial')

    time = traces[0][0]
    fs = traces[1]
    ps = traces[2]

    f_rows = zip(*([time] + list(fs)))
    p_rows = zip(*([time] + list(ps)))

    _write_results(f_output_filename, f_rows, 'Time', '[F-actin]',
            'Cooperativity', labels)

    _write_results(p_output_filename, p_rows, 'Time', '[Pi]',
            'Cooperativity', labels)

def _write_results(filename, rows, x_name, y_name, column_name, column_ids):
    with open(filename, 'w') as f:
        # Header lines, identifying x, y, column name
        f.write('# Auto-collated output:\n')
        f.write('# x: %s\n' % x_name)
        f.write('# y: %s\n' % y_name)
        f.write('# columns: %s\n' % column_name)
#        f.write('#     %s\n\n' % column_ids)
        f.write('#     ')
        f.write(str(column_ids))
        f.write('\n\n')
        # CSV dump of actual data
        w = csv.writer(f, dialect=data.DatDialect)
        w.writerows(rows)


def _get_best_tc(session_id, alpha):
    rates, chi2s = get_xy(session_id)
    rate_pack, k_pack, c_pack = fit_xy(rates, chi2s, alpha)

    import bisect
    xi = bisect.bisect(rates, rate_pack[0])
    nearest_rate = rates[xi]

    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)
    runs = session.experiments[0].runs
    nearest_run = None
    for run in runs:
        if run.parameters['release_rate'] == nearest_rate:
            nearest_run = run
            break;

    t, f, p, fe, pe = _get_timecourses(nearest_run)
    cooperativity = session.parameters.get('release_cooperativity', None)

    return cooperativity, t, f, p

def plot_best_timecourses(session_ids, alpha=0.01, colors=['b', 'r', 'g']):
    import pylab
    f = pylab.figure()
    a = f.add_subplot(1, 1, 1)

    f_data = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/factin_concentration.dat')
    p_data = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/phosphate_concentration.dat')
    pv = numpy.array(p_data[1])
    a.fill_between(p_data[0], 0.9 * pv, 1.1 * pv, color='#BBBBBB')
    a.plot(f_data[0], f_data[1], 'k-', label='Data')
    a.plot(p_data[0], pv, 'k--')
    
    for sid, color in zip(session_ids, colors):
        _plot_nf_timecourse(sid, axes=a, alpha=alpha, color=color)

    a.set_ylim([0, 35])
    a.legend(loc=4)
    a.set_xlabel('Time [s]')
    a.set_ylabel(r'Concentrations [$\mu$M]')

def _plot_nf_timecourse(session_id, axes=None, alpha=None, color=None):
    rates, chi2s = get_xy(session_id)
    rate_pack, k_pack, c_pack = fit_xy(rates, chi2s, alpha)

    import bisect
    xi = bisect.bisect(rates, rate_pack[0])
    nearest_rate = rates[xi]

    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)
    runs = session.experiments[0].runs
    nearest_run = None
    for run in runs:
        if run.parameters['release_rate'] == nearest_rate:
            nearest_run = run
            break;

    t, f, p, fe, pe = _get_timecourses(nearest_run)
    cooperativity = session.parameters.get('release_cooperativity', None)
    if cooperativity is not None:
        label = r'$\rho_d$ = %.2e' % cooperativity
    else:
        label = 'Vectorial'

    axes.plot(t, f, color + '-', label=label)
    axes.plot(t, p, color + '--')


def _get_timecourses(run):
    times, factin, f_err = run.analyses['factin']
    times, pi, pi_err = run.analyses['Pi']

    return times, factin, pi, f_err, pi_err

def _make_filename(cooperativity):
    if cooperativity:
        return 'fit_rho_%.0e.eps' % cooperativity
    return 'fit_vectorial.eps'

def save_plots(session_ids, alpha=0.01):
    for sid in session_ids:
        try:
            plot_fit(sid, interactive=False, alpha=alpha)
        except:
            pass
