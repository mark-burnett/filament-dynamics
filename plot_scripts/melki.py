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
#    with contexts.complex_figure('plots/melki_rates_combined.eps',
#            width=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM,
#            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2,
#            right_label=True) as figure:
#        melki_rate_plot(figure)
#        melki_rate_error_plot(figure)
#    melki_timecourses()
    single_timecourse()
#    stupid_melki_timecourses()


def melki_rate_plot(figure):
    results = data.load_data('results/melki_rates.dat')
#    results = data.load_data('results/melki_rate_sensitivities.dat')
#    cooperativities, rates, statistical_errors, halftimes, hte = results
#    cooperativities, rates, errors = results[:3]
    cooperativities, rates = results[:2]

#    with contexts.basic_figure('plots/melki_rates.eps',
    with contexts.subplot(figure, (2, 1, 1), title='A',
#            x_label=r'Pi Dissociation Cooperativity, $\rho_d$',
            y_label=r'Non-Boundary Pi Dissociation Rate, $r_d$ [$s^{-1}$]',
            logscale_x=True, logscale_y=True) as axes:
        contexts.plot(axes, 'plot', cooperativities, rates, 'k.')
#        contexts.plot(axes, 'errorbar', cooperativities, rates,
#                errors, fmt='k.')

        cooperativities = numpy.array(cooperativities)
        contexts.plot(axes, 'plot',
                cooperativities, 1.0 / (388 * numpy.sqrt(cooperativities)),
                'r-', linewidth=0.5)

        axes_2 = axes.twinx()
        axes_2.set_yscale('log')
        axes_2.set_ylabel(r'Boundary Pi Dissociation Rate, $R_d$ [$s^{-1}$]',
                size=settings.LABEL_FONT_SIZE)
        for label in axes_2.get_yticklabels():
            label.set_size(settings.TICK_FONT_SIZE)

        axes.axvline(69444444, 0, 1, linestyle='--', color='g', linewidth=0.5)


        contexts.plot(axes_2, 'plot', cooperativities,
                cooperativities * rates, 'k.', markerfacecolor='None')

        axes_2.axhline(24, 0, 1, linestyle=':', color='b')

        axes.set_xlim([0.1, 10**12])

        axes.set_xticks([1, 100, 10000, 1000000,
            100000000, 10000000000])
        


        

def melki_rate_error_plot(figure):
    results = data.load_data('results/melki_rate_sensitivities.dat')
    cooperativities, rates, errors = results[:3]

    theoretical_rates = 1.0 / (388 * numpy.sqrt(cooperativities))
    rates = numpy.array(rates) / theoretical_rates
    errors = numpy.array(errors) / theoretical_rates

#    with contexts.basic_figure('plots/melki_rate_errors.eps',
    with contexts.subplot(figure, (2, 1, 2), title='B',
            x_label=r'Pi Dissociation Cooperativity, $\rho_d$',
            y_label=r'$r_d$ [Simulation / Theory]',
            logscale_x=True,
#            logscale_y=True
            ) as axes:
        contexts.plot(axes, 'errorbar', cooperativities,
                rates, errors, fmt='k.')
        contexts.plot(axes, 'plot', cooperativities,
                [1 for c in cooperativities], 'r-')

        axes.axvline(69444444, 0, 1, linestyle='--', color='g', linewidth=0.5)

        axes.set_xlim([0.1, 10**12])

        axes.set_xticks([1, 100, 10000, 1000000,
            100000000, 10000000000])
        

#        axes.set_xlim([0.1, 10000000])
#
#        axes.set_xticks([1, 10, 100, 1000, 10000, 100000, 1000000])



def stupid_melki_timecourses():
    factin_sims = data.load_data('results/melki_factin_timecourses.dat')
    pi_sims = data.load_data('results/melki_pi_timecourses.dat')
    fs_cdot, f_rho_1e0, f_rho_1e3, f_rho_1e6 = factin_sims
    ps_cdot, p_rho_1e0, p_rho_1e3, p_rho_1e6 = pi_sims

    np_sims = data.load_data('results/new_melki_pi_timecourses.dat')
    nps_cdot, np_rho_1e0 = np_sims

    f_data = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/factin_concentration.dat')
    p_data = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/phosphate_concentration.dat')
    fd_cdot, fd_f = f_data
    pd_cdot, pd_p = p_data

    scaled_pd_p = pd_p

    with contexts.basic_figure('plots/melki_timecourses.eps',
            x_label=r'Time [s]',
            y_label=r'Phosphate Concentration [$\mu$M]') as axes:
        contexts.plot(axes, 'plot', pd_cdot, scaled_pd_p, 'k-',
                label='Data')

        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e0, 'r:',
                label=r'$r_d=0.00204$, $t_\frac{1}{2}=388$')

        contexts.plot(axes, 'plot', nps_cdot, np_rho_1e0, 'b:',
                label=r'$r_d=0.00179$, $t_\frac{1}{2}=433$')

        axes.set_xlim([0, 2500])
        axes.set_ylim([0, 35])

        contexts.add_legend(axes, loc='lower right')



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

#    scaled_pd_p = _scale_data_to(pd_p, 30)
    s_scaled_pd_p = _scale_data_to(pd_p, p_rho_1e0[-1] * 1.010)
    scaled_pd_p = pd_p

    with contexts.basic_figure('plots/melki_timecourses.eps',
            x_label=r'Time [s]',
            y_label=r'Phosphate Concentration [$\mu$M]') as axes:
#        contexts.plot(axes, 'plot', fd_cdot, fd_f, 'k-')#, label='Data')
#        contexts.plot(axes, 'plot', pd_cdot, scaled_pd_p, 'k:')
        contexts.plot(axes, 'plot', pd_cdot, scaled_pd_p, 'k--',
                label='Data')
#        contexts.plot(axes, 'plot', pd_cdot, pd_p, 'k-')
        contexts.plot(axes, 'plot', pd_cdot, s_scaled_pd_p, 'k-',
                label='Scaled Data')

#        contexts.plot(axes, 'plot', fs_cdot, f_rho_1e0, 'r-',
#                label=r'$\rho_d =\,1$')
#        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e0, 'r:')
        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e0, 'r:',
                label=r'$\rho_d =\,1$')

#        contexts.plot(axes, 'plot', fs_cdot, f_rho_1e3, 'g-',
#                label=r'$\rho_d =\,10^3$')
#        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e3, 'g:')
        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e3, 'g--',
                label=r'$\rho_d =\,2$')

#        contexts.plot(axes, 'plot', fs_cdot, f_rho_1e6, 'b-',
#                label=r'$\rho_d =\,10^6$')
#        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e6, 'b:')
        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e6, 'b-.',
                label=r'$\rho_d =\,10$')

#        contexts.plot(axes, 'plot', ps_cdot, p_rho_1e6, 'k-.',
#                label=r'$\rho_d =\,10$')

        axes.set_xlim([0, 2500])
        axes.set_ylim([0, 35])

        contexts.add_legend(axes, loc='lower right')

def single_timecourse():
    sim = data.load_data('results/timecourses.dat')
    stime, sfactin, spi = sim

    f_data = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/factin_concentration.dat')
    p_data = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/phosphate_concentration.dat')
    fd_cdot, fd_f = f_data
    pd_cdot, pd_p = p_data

    with contexts.basic_figure('plots/crazy_timecourses.eps',
            x_label=r'Time [s]',
            y_label=r'Phosphate Concentration [$\mu$M]') as axes:
        contexts.plot(axes, 'plot', pd_cdot, pd_p, 'r-', label='Data [Pi]')
        contexts.plot(axes, 'plot', stime, spi, 'r:', label='Simulated [Pi]')

        contexts.plot(axes, 'plot', fd_cdot, fd_f, 'k-', label='Data [F-actin]')
        contexts.plot(axes, 'plot', stime, sfactin, 'k:', label='Simulated [F-actin]')

        axes.set_xlim([0, 2500])
        axes.set_ylim([0, 35])

        contexts.add_legend(axes, loc='lower right')


def _scale_data_to(data, final_value):
    result = numpy.array(data)
    current_final_value = data[-1]
    result *= float(final_value) / current_final_value
    return result


if '__main__' == __name__:
    main()
