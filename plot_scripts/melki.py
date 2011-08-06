#! /usr/bin/env python
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

#from matplotlib import pyplot
import matplotlib

matplotlib.use('AGG')

from matplotlib import pyplot

import numpy
import scipy

from actin_dynamics.io import data
from actin_dynamics.numerical import meshes

from plot_scripts import settings

def main():
    melki_rate_plot()
    melki_timecourses()


def melki_rate_plot():
    results = data.load_data('results/melki_rates.dat')
    cooperativities, rates, statistical_errors, mesh_errors = results

    total_errors = numpy.array(statistical_errors) + numpy.array(mesh_errors)
    pyplot.figure()
    pyplot.errorbar(cooperativities, rates, yerr=total_errors,
            fmt='ro', label='Simulation Result')

    fit_x, fit_y, polynomial = rate_fit(cooperativities, rates, 2)
    poly_label = make_poly_fit_label(polynomial)
    pyplot.plot(fit_x, fit_y, label=poly_label)


    pyplot.xlabel(r'Phosphate Dissociation Cooperativity, $\rho_d$')
    pyplot.ylabel(r'Phosphate Dissociation Rate, $r_d$ [$s^{-1}$]')

    pyplot.xscale('log')
    pyplot.yscale('log')
    pyplot.xlim([0.1, 10000000])
    pyplot.ylim([1e-6, 0.01])

    pyplot.legend(loc='lower left')

    pyplot.savefig('plots/melki_rates.eps', dpi=settings.DPI)


def melki_timecourses():
    factin_sims = data.load_data('results/melki_factin_timecourses.dat')
    pi_sims = data.load_data('results/melki_pi_timecourses.dat')
    fs_cdot, f_rho_1e0, f_rho_1e3, f_rho_1e6 = factin_sims
    ps_cdot, p_rho_1e0, p_rho_1e3, p_rho_1e6 = pi_sims

    f_data = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/factin_concentration.dat')
    p_data = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/phosphate_concentration.dat')
    fd_cdot, fd_f = f_data
    pd_cdot, pd_p = p_data

    pyplot.figure()
    # Data
    pyplot.plot(fd_cdot, fd_f, 'k-',
            linewidth=settings.BOLD_LINE_WIDTH,
            label='[F-actin] Data')
    pyplot.plot(pd_cdot, pd_p, 'k.',
            linewidth=settings.BOLD_LINE_WIDTH,
            label='[Pi] Data')

    # Rho = 1
    pyplot.plot(fs_cdot, f_rho_1e0, 'r-',
            label=r'$\rho_d = 1$ [F-actin] Simulation',
            linewidth=settings.NORM_LINE_WIDTH)
    pyplot.plot(ps_cdot, p_rho_1e0, 'r.',
            label=r'$\rho_d = 1$ [Pi] Simulation',
            linewidth=settings.NORM_LINE_WIDTH)

    # Rho = 1000
    pyplot.plot(fs_cdot, f_rho_1e3, 'g-',
            label=r'$\rho_d = 1000$ [F-actin] Simulation',
            linewidth=settings.NORM_LINE_WIDTH)
    pyplot.plot(ps_cdot, p_rho_1e3, 'g.',
            label=r'$\rho_d = 1000$ [Pi] Simulation',
            linewidth=settings.NORM_LINE_WIDTH)

    # Rho = 1000000
    pyplot.plot(fs_cdot, f_rho_1e6, 'b-',
            label=r'$\rho_d = 1000000$ [F-actin] Simulation',
            linewidth=settings.NORM_LINE_WIDTH)
    pyplot.plot(ps_cdot, p_rho_1e6, 'b.',
            label=r'$\rho_d = 1000000$ [Pi] Simulation',
            linewidth=settings.NORM_LINE_WIDTH)

    pyplot.xlim([0, 2500])
    pyplot.ylim([0, 35])

    # XXX Units font is not to be perfect/uniform.
    pyplot.xlabel('Time [s]')
    pyplot.ylabel(r'Concentration [$\mu M$]')

    pyplot.legend(loc='lower right')

    pyplot.savefig('plots/melki_timecourses.eps', dpi=settings.DPI)



def rate_fit(cooperativities, rates, degree, mesh_factor=3):
    l_x = numpy.log(cooperativities)
    l_y = numpy.log(rates)

    f_x = meshes.make_mesh(cooperativities[0], cooperativities[-1],
            mesh_factor * len(cooperativities), 'log')
    poly_x = numpy.log(f_x)

    polynomial = scipy.polyfit(l_x, l_y, degree)
    poly_y = scipy.polyval(polynomial, poly_x)

    f_y = numpy.exp(poly_y)

    return f_x, f_y, polynomial


def make_poly_fit_label(polynomial):
    degree = len(polynomial) - 1
    expression = None
    for i, a in enumerate(polynomial):
        val = transform_value(numpy.abs(a))
        exponent = degree - i

        if a < 0:
            sign = '-'
        else:
            sign = '+'

        if exponent > 1:
            this_part = r'%s\cdot\,(\ln{\,\rho_d})^%d' % (val, exponent)
        elif 1 == exponent:
            this_part = r'%s\cdot\,\ln{\,\rho_d}' % val
        else:
            this_part = r'%s' % val

        if i:
            expression = r'%s %s\,%s' % (expression, sign, this_part)
        else:
            if a < 0:
                expression = r'-%s' % this_part
            else:
                expression = this_part

    if expression:
        return r'$r_d = e^{%s}$' % expression
    else:
        return r'$r_d = 1$'

def transform_value(value):
    basic_string = '%e' % value

    coefficient, exponent = basic_string.split('e')

    f_coef = float(coefficient)
    i_expo = int(exponent)

    if 1 == i_expo:
        return r'%.2f \cdot 10' % f_coef
    elif 0 == i_expo:
        return r'%.2f' % f_coef
    else:
        return r'%.2f \cdot 10^{%d}' % (f_coef, i_expo)


if '__main__' == __name__:
    main()
