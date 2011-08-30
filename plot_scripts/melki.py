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

import pprint

import numpy
import scipy

from actin_dynamics.io import data
from actin_dynamics.numerical import meshes

from plot_scripts import contexts
from plot_scripts import settings

def main():
    melki_rate_plot()
    melki_timecourses()


def melki_rate_plot():
    results = data.load_data('results/melki_rates.dat')
    cooperativities, rates, statistical_errors, mesh_errors = results

    total_errors = numpy.array(statistical_errors) + numpy.array(mesh_errors)

    with contexts.basic_figure('plots/melki_rates.eps',
            x_label=r'Pi Dissociation Cooperativity, $\rho_d$',
            y_label=r'Pi Dissociation Rate, $r_d$ [$s^{-1}$]',
            logscale_x=True, logscale_y=True) as axes:
        contexts.plot(axes, 'errorbar', cooperativities, rates,
                total_errors, fmt='k.')
#                , label='Simulation Result')

        fit_x, fit_y, polynomial = rate_fit(cooperativities, rates, 2)
        poly_label = make_poly_fit_label(polynomial)
        contexts.plot(axes, 'plot', fit_x, fit_y, 'k-', label=poly_label)

        axes.set_xlim([0.1, 10000000])
        axes.set_ylim([1e-5, 0.01])

        axes.set_xticks([1, 10, 100, 1000, 10000, 100000, 1000000])
        axes.set_xticklabels([r'$10^{0}$', r'$10^{1}$', r'$10^2$', r'$10^3$',
            r'$10^4$', r'$10^5$', r'$10^6$'])

        axes.text(1, 4e-3, poly_label, fontsize=settings.SMALL_FONT_SIZE)

#        contexts.add_legend(axes, loc='lower left', dashlength=0)

#        axes.legend(loc='lower left')


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

    scaled_pd_p = _scale_data_to(pd_p, 30)

    with contexts.basic_figure('plots/melki_timecourses.eps',
            x_label=r'Time [s]',
            y_label=r'Phosphate Concentration [$\mu$M]') as axes:
#        contexts.plot(axes, 'plot', fd_cdot, fd_f, 'k-')#, label='Data')
#        contexts.plot(axes, 'plot', pd_cdot, scaled_pd_p, 'k:')
        contexts.plot(axes, 'plot', pd_cdot, scaled_pd_p, 'k-',
                label='Data')

#        contexts.plot(axes, 'plot', fs_cdot, f_rho_1e0, 'r-',
#                label=r'$\rho_d =\,1$')
#        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e0, 'r:')
        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e0, 'r:',
                label=r'$\rho_d =\,1$')

#        contexts.plot(axes, 'plot', fs_cdot, f_rho_1e3, 'g-',
#                label=r'$\rho_d =\,10^3$')
#        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e3, 'g:')
        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e3, 'g--',
                label=r'$\rho_d =\,10^3$')

#        contexts.plot(axes, 'plot', fs_cdot, f_rho_1e6, 'b-',
#                label=r'$\rho_d =\,10^6$')
#        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e6, 'b:')
        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e6, 'b-.',
                label=r'$\rho_d =\,10^6$')

        axes.set_xlim([0, 2500])
        axes.set_ylim([0, 35])

        contexts.add_legend(axes, loc='lower right')



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
        return r'$r_d \approx\,e^{%s}$' % expression
    else:
        return r'$r_d \approx\,1$'

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


def _scale_data_to(data, final_value):
    result = numpy.array(data)
    current_final_value = data[-1]
    result *= float(final_value) / current_final_value
    return result


if '__main__' == __name__:
    main()
