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

import math
import operator
import numpy
import scipy
import scipy.stats

from actin_dynamics.io import data

from actin_dynamics import database
from actin_dynamics.numerical import utils

MAX_AT_ZERO = 876.3
MAX_AT_INF = 99.96

INITIAL_B = 0.0003
INITIAL_D = 0.03

def _func(x, b, d):
    return (MAX_AT_ZERO * numpy.exp(-x / b) +
            MAX_AT_INF * (1 - numpy.exp(-x / d)))

def _fit_func(pars, x_values, y_values):
    b, d = pars
    f_values = _func(x_values, b, d)
    return ((f_values - y_values)**2).sum()

def _minimum(pars):
    b, d = pars
    x = b * d / (d - b) * numpy.log(MAX_AT_ZERO * d / (MAX_AT_INF * b))
    y = _func(x, b, d)

    return x, y

def error_roots(coeffs, number_of_filaments, delta=0.01):
    a, b, c = coeffs
    best_parameter = -b / (2 * a)
    best_error = float(scipy.polyval(coeffs, best_parameter))

    par_minus = best_parameter * (1 - delta)
    par_plus = best_parameter * (1 + delta)

#    print 'pm', par_minus
#    print 'bp', best_parameter
#    print 'pp', par_plus

    cval_plus = float(scipy.polyval(coeffs, par_plus))

    cval_minus = float(scipy.polyval(coeffs, par_minus))

    dx = best_parameter * delta
#    print 'dy', cval_plus - best_error
#    print 'dx', dx
    sens_plus = (cval_plus - best_error) / dx
    sens_minus = (cval_minus - best_error) / dx

    sens = min(sens_plus, sens_minus)

    y_error = 1 / numpy.sqrt(number_of_filaments)
#    print 'yerr', y_error, best_error
    pct_error = y_error / sens
    return pct_error
#    print 'eps', epsilon
#    print 'pct error', epsilon / best_parameter

    return best_parameter - epsilon, best_parameter + epsilon


    return low, high

def fmin_objective(c, a, b, x_values, y_values):
    '''For fitting a parabola with minimum fixed at x = minimum
    '''
    return ((y_values - scipy.polyval([a, b, c], x_values))**2).sum()

def regula_objective(parameter, coeffs, alpha_target, n, x_values, y_values):
    '''For fitting parameter such that alpha = alpha_target.
    '''
    a, base_b, c = coeffs
    b = - 2 * a * parameter
    par, fv, numiter, funcalls, warnflag = scipy.optimize.fmin(
            fmin_objective, c, args=(a, b, x_values, y_values),
            full_output=1, disp=0)

    ro_alpha = scipy.stats.chi2.cdf(fv, n)
#    print 'at', alpha_target, 'ra', ro_alpha
    v = alpha_target - ro_alpha
#    print 'v', v
    return v
    

def fit_errors(best_coeffs, alpha, n, x_values, y_values):
    best_par = - best_coeffs[1] / (2 * best_coeffs[0])
    min_par = scipy.optimize.ridder(regula_objective,
            0.5 * best_par, best_par,
            args=(best_coeffs, alpha, n, x_values, y_values),
            disp=False)
    max_par = scipy.optimize.ridder(regula_objective,
            best_par, 2 * best_par,
            args=(best_coeffs, alpha, n, x_values, y_values),
            disp=False)

    return min_par, max_par

def get_fits(session_ids, alpha=0.1, output_filename='results/chifits.dat'):
    results = []
    for sid in session_ids:
        vals = smart_fit(sid, alpha=alpha)
        if vals is not None:
            results.append(vals)

    results.sort()

    _small_writer(output_filename, results,
            ['Cooperativity', 'Best Rate', 'Bottom CI', 'Top CI', 'Chi^2'],
            header='# alpha = %s\n' %alpha)

    return results

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


def get_xy(session_id):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)
    runs = session.experiments[0].runs

    pairs = sorted([(r.get_objective('pi_fit'), r.parameters['release_rate'])
            for r in runs if (r.get_objective('pi_fit') is not None
                and not math.isnan(r.get_objective('pi_fit'))
                and r.get_objective('pi_fit') < 6)],
            key = operator.itemgetter(1))

    y_values, x_values = zip(*pairs)
    x_values = numpy.array(x_values)
    y_values = numpy.array(y_values)

    return x_values, y_values


def smart_fit(session_id, alpha=0.1):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)
    runs = session.experiments[0].runs

    pairs = sorted([(r.get_objective('pi_fit'), r.parameters['release_rate'])
            for r in runs if (r.get_objective('pi_fit') is not None
                and not math.isnan(r.get_objective('pi_fit'))
                and r.get_objective('pi_fit') < 6)],
            key = operator.itemgetter(1))
    if 10 > len(pairs):
        return None

    y_values, x_values = zip(*pairs)
    x_values = numpy.array(x_values)
    y_values = numpy.array(y_values)

    coeffs, R2, n, svs, rcond = scipy.polyfit(x_values, y_values, 2, full=True)
#    print 'coeffs', coeffs
#    print 'best R2', R2

#    alpha = float(scipy.stats.chi2.cdf(R2, n))
#    print 'extracted alpha =', alpha

    best_parameter = - coeffs[1] / (2 * coeffs[0])
    best_error = scipy.polyval(coeffs, best_parameter)

#    num_filaments = runs[0].all_parameters['number_of_filaments']
#    pct_error = error_roots(coeffs, num_filaments)
#    print 'percent error of rate =', 100 * pct_error

#    par_guess = (coeffs[0], coeffs[2])

#    print 'alpha_target = 0.1 -> R2 =', scipy.stats.chi2.ppf(0.1, n)

    min_par, max_par = fit_errors(coeffs, alpha, n, x_values, y_values)

    cooperativity = runs[0].all_parameters.get('release_cooperativity', None)

    return cooperativity, best_parameter, min_par, max_par, best_error

#    print 'best par', best_parameter
#    print 'CI', min_par, max_par

##    new_coeffs = regula_objective(
##            0.97 * best_parameter, coeffs, 0.1, n, x_values, y_values)
##    print 'new_coeffs', new_coeffs
#
#    f_values = scipy.polyval(coeffs, x_values)
#
#
#    f_fit_diff = (f_values - y_values)
##    print 'mean =', numpy.mean(f_fit_diff)
##    print 'avg variance =', numpy.var(f_fit_diff)
##    print 'expected variance =', numpy.mean(f_values**2 / num_filaments)
#
#    # Divide by the actual standard deviation
#    f_fit_diff /= numpy.std(f_fit_diff)
#    f_fit_diff = f_fit_diff**2
#
#    # Divide by the expected variance
##    f_fit_diff /= (f_values**2 / num_filaments)
#
#    f_fit_diff.sort()
#
#    chi_cdf = numpy.array(list(utils.running_total(f_fit_diff)))/len(f_fit_diff)
#    cdf = scipy.stats.chi2.cdf(f_fit_diff, n)
#
#    import matplotlib.pyplot
#    pyplot = matplotlib.pyplot
#    pyplot.subplot(2, 1, 1)
#    pyplot.plot(x_values, y_values, 'r.')
#    pyplot.plot(x_values, f_values, 'b-')
##    pyplot.plot(x_values, scipy.polyval(new_coeffs, x_values), 'g-')
#
#    pyplot.axvline(best_parameter, 0, 1,
#            color='g', linestyle=':', linewidth=0.5)
#
#    a2 = pyplot.subplot(2, 1, 2)
##    a2.set_yscale('log')
#
#    pyplot.plot(f_fit_diff, chi_cdf, 'r-')
#    pyplot.plot(f_fit_diff, cdf, 'b-')
#
#    pyplot.show()


def dump_fit_quality(session_ids):
    dbs = database.DBSession()

    sessions = [dbs.query(database.Session).get(session_id)
            for session_id in session_ids]
