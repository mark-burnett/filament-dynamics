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

HALFTIME = 433
#RHO_CRIT = 69444444
RHO_CRIT = (15/0.00167)**2

MELKI_ERROR = 0.1

def main():
    with contexts.complex_figure('plots/melki_rates_combined.pdf',
            width=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM,
            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2,
            right_label=True) as figure:
        melki_rate_plot(figure)
        melki_rate_error_plot(figure)
#    melki_timecourses()
#    single_timecourse()
#    stupid_melki_timecourses()
    with contexts.complex_figure('plots/melki_fit_quality.pdf',
            width=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM,
            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2) as figure:
        melki_rate_fit_quality(figure)
        melki_sample_timecourses(figure)



def melki_rate_plot(figure):
#    results = data.load_data('results/melki_rates.dat')
    results = data.load_data('results/melki_cooperative_fit.dat')
    v_results = data.load_data('results/melki_vectorial_fit.dat')

#    results = data.load_data('results/melki_rate_sensitivities.dat')
#    cooperativities, rates, statistical_errors, halftimes, hte = results
#    cooperativities, rates, errors = results[:3]
    cooperativities, rates = results[:2]
    v_rate_pack = zip(*v_results)[0][:3]

#    with contexts.basic_figure('plots/melki_rates.pdf',
    with contexts.subplot(figure, (2, 1, 1), title='A',
#            x_label=r'Pi Dissociation Cooperativity, $\rho_d$',
            y_label=r'Non-Boundary Pi Dissociation Rate, $r_d$ [$s^{-1}$]',
            logscale_x=True, logscale_y=True) as axes:
        contexts.plot(axes, 'plot', cooperativities, rates, 'k.')
#        contexts.plot(axes, 'errorbar', cooperativities, rates,
#                errors, fmt='k.')

        cooperativities = numpy.array(cooperativities)
        contexts.plot(axes, 'plot',
                cooperativities, 1.0 / (HALFTIME * numpy.sqrt(cooperativities)),
                'r-', linewidth=0.5)

        axes_2 = axes.twinx()
        axes_2.set_yscale('log')
        axes_2.set_ylabel(r'Boundary Pi Dissociation Rate, $R_d$ [$s^{-1}$]',
                size=settings.LABEL_FONT_SIZE)
        for label in axes_2.get_yticklabels():
            label.set_size(settings.TICK_FONT_SIZE)

        axes.axvline(RHO_CRIT, 0, 1, linestyle='--', color='g', linewidth=0.5)


        contexts.plot(axes_2, 'plot', cooperativities,
                cooperativities * rates, 'k.', markerfacecolor='None')

        axes_2.axhline(v_rate_pack[0], 0, 1, linestyle=':', color='b')
        axes_2.set_ylim([1.0e-4, 100])

        axes.set_xlim([0.1, 10**12])

        axes.set_xticks([1, 100, 10000, 1000000,
            100000000, 10000000000])
        


        

def melki_rate_error_plot(figure):
#    results = data.load_data('results/melki_rate_sensitivities.dat')
    results = data.load_data('results/melki_cooperative_fit.dat')
    cooperativities, rates, min_rates, max_rates = results[:4]

    theoretical_rates = 1.0 / (HALFTIME * numpy.sqrt(cooperativities))
    errors = numpy.array(numpy.array(rates) - numpy.array(min_rates)) / theoretical_rates
    rates = numpy.array(rates) / theoretical_rates

#    with contexts.basic_figure('plots/melki_rate_errors.pdf',
    with contexts.subplot(figure, (2, 1, 2), title='B',
            x_label=r'Pi Dissociation Cooperativity, $\rho_d$',
            y_label=r'$r_d$ [Simulation / Theory]',
            logscale_x=True,
#            logscale_y=True
            ) as axes:
        axes.axvline(RHO_CRIT, 0, 1, linestyle='--', color='g', linewidth=0.5)

        contexts.plot(axes, 'errorbar', cooperativities,
                rates, errors, fmt='k.')
        contexts.plot(axes, 'plot', cooperativities,
                [1 for c in cooperativities], 'r-', linewidth=0.5)

        axes.set_xlim([0.1, 10**12])

        axes.set_xticks([1, 100, 10000, 1000000,
            100000000, 10000000000])
        

        axes.set_ylim([0, 1.2])
#        axes.set_xlim([0.1, 10000000])
#
#        axes.set_xticks([1, 10, 100, 1000, 10000, 100000, 1000000])

def melki_rate_fit_quality(figure):
    results = data.load_data('results/melki_cooperative_fit.dat')
    (cooperativities, rates, min_rates, max_rates, rate_pe,
            chi2, min_chi2, max_chi2, chi2_pe) = results
    v_results = data.load_data('results/melki_vectorial_fit.dat')
    (v_rate, junk, junk, junk,
            v_chi2, v_min_chi2, v_max_chi2, junk) = zip(*v_results)[0]
    with contexts.subplot(figure, (2, 1, 2), title='B',
            x_label=r'Pi Dissociation Cooperativity, $\rho_d$',
            y_label=r'$\chi^2$ Comparison To Data',
            logscale_x=True) as axes:
        axes.fill_between([0.1, 1.0e12],
                [v_min_chi2, v_min_chi2],
                v_max_chi2, color='#CCCCFF')
        axes.axhline(v_chi2, 0, 1, linestyle=':', color='b')
        axes.axvline(RHO_CRIT, 0, 1, linestyle='--', color='g', linewidth=0.5)

        contexts.plot(axes, 'errorbar', cooperativities,
                chi2, [c - m for c, m in zip(chi2, min_chi2)],
                fmt='k.')

        axes.set_xlim([0.1, 10**12])
        axes.set_ylim([0, 14])

        axes.set_xticks([1, 100, 10000, 1000000,
            100000000, 10000000000])

def melki_sample_timecourses(figure):
    data_f_times, data_f = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/factin_concentration.dat')
    data_p_times, data_p = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/phosphate_concentration.dat')
    data_p = numpy.array(data_p)

    sim_f = data.load_data('results/melki_timecourses_f.dat')
    sim_p = data.load_data('results/melki_timecourses_p.dat')
    sf_times, sf_vals = sim_f[0], sim_f[1:]
    sp_times, sp_vals = sim_p[0], sim_p[1:]

    colors = ['b', 'g', 'r', 'orange']
    labels = ['Vectorial', 'Random', r'$\rho_d = 10^4$', r'$\rho_d = 10^8$']

    with contexts.subplot(figure, (2, 1, 1), title='A',
            x_label=r'Time [s]',
            y_label=r'Concentrations [$\mu$M]') as axes:
        axes.fill_between(data_p_times,
                data_p * (1 - MELKI_ERROR), data_p * (1 + MELKI_ERROR),
                color='#CCCCCC')
        axes.plot(data_f_times, data_f, 'k--')
        axes.plot(data_p_times, data_p, 'k-', label='Data')

        for f, p, c, l in zip(sf_vals, sp_vals, colors, labels):
            axes.plot(sf_times, f, color=c, linestyle='--')
            axes.plot(sp_times, p, color=c, linestyle='-', label=l)

        axes.set_ylim([0, 35])
        axes.set_xlim([0, 2500])

        l = axes.legend(loc=4)
        l.draw_frame(False)


if '__main__' == __name__:
    main()
