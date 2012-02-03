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


def get_xy(session_id):
    dbs = database.DBSession()
    session = dbs.query(database.Session).get(session_id)
    runs = session.experiments[0].runs

    pairs = sorted([(r.get_objective('pi_fit'), r.parameters['release_rate'])
            for r in runs if r.get_objective('pi_fit') is not None],
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


def linear_fit(session_id, alpha, method='OLS'):
    x_values, y_values = get_xy(session_id)

    xp = numpy.vander(x_values, 3)
    model = getattr(sm, method)(y_values, xp)
    fitresult = model.fit('qr')
    a, b, c = fitresult.params
    aci, bci, cci = fitresult.conf_int(alpha=alpha)

    rate = -b / (2 * a)

    # Remember max(bci) will give the min(abs(bci))
    min_rate = -max(bci) / (2 * max(aci))
    max_rate = -min(bci) / (2 * min(aci))

    pct_error =  100 * (max_rate - rate) / rate

    chi2 = scipy.polyval(fitresult.params, rate)

    cooperativity = get_parameter(session_id, 'release_cooperativity')

    return cooperativity, rate, min_rate, max_rate, pct_error, chi2


def covariance_fit(session_id, alpha):
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

    return cooperativity, rate, min_rate, max_rate, rate_pct_error, c, min_c, max_c, c_pct_error


def manual_fit(session_id, alpha):
    x_values, y_values = get_xy(session_id)

    coeffs = scipy.polyfit(x_values, y_values, 2)

    x4 = (x_values**4).sum()
    x3 = (x_values**3).sum()
    x2 = (x_values**2).sum()
    x1 = x_values.sum()
    n = len(x_values)

    A = numpy.array([[ n, x1, x2],
                     [x1, x2, x3],
                     [x2, x3, x4]])

    Ai = numpy.linalg.inv(A)

    yvar = ((y_values - scipy.polyval(coeffs, x_values))**2).sum() / (n - 3)

    vcv = yvar * Ai

    a, b, c = coeffs

    d = numpy.array([[0],
                     [-1/(2*a)],
                     [b/(2*a**2)]])
    std_err = float(numpy.sqrt(numpy.dot(d.transpose(), numpy.dot(vcv, d))))
    t = scipy.stats.t.ppf(1 - alpha/2, len(x_values) - 3)
    rate = -b/(2*a)
    
    min_rate = rate - t * std_err
    max_rate = rate + t * std_err

    pct_error =  100 * (max_rate - rate) / rate
    cooperativity = get_parameter(session_id, 'release_cooperativity')

    chi2 = scipy.polyval(coeffs, rate)

    return cooperativity, rate, min_rate, max_rate, pct_error, chi2


def save_fits(cooperative_ids, vectorial_id, alpha=0.05,
        cooperative_filename='results/melki_cooperative_fit.dat',
        vectorial_filename='results/melki_vectorial_fit.dat'):
    coop_results = []
    for cid in cooperative_ids:
        coop_results.append(covariance_fit(cid, alpha=alpha))
    coop_results.sort()
    _small_writer(output_filename, coop_results,
            ['Cooperativity', 'Rate', 'Min Rate', 'Max Rate', '% Error', 'Chi^2'],
            header='# Fit of cooperative models to Melki data\n# alpha = %s' % alpha)

    vec_results = [covariance_fit(vectorial_id, alpha=alpha)[1:]]
    _small_writer(output_filename, vec_results,
            ['Rate', 'Min Rate', 'Max Rate', '% Error', 'Chi^2'],
            header='# Fit of vectorial model to Melki data\n# alpha = %s' % alpha)
