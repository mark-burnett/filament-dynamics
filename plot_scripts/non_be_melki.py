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
    with contexts.complex_figure('plots/melki_non_be_comparison.pdf',
            width=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM,
            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2) as figure:
        non_be_rates(figure)
        non_be_quality(figure)


def non_be_rates(figure):
    results = data.load_data('results/melki_cooperative_fit.dat')
    nb_results = data.load_data('results/melki_non_be_coop_fit.dat')
    nop_results = data.load_data('results/melki_no_pointed_coop_fit.dat')
    cooperativities, rates, min_rates, max_rates = results[:4]
    nbc, nbr, nb_minr, nb_maxr = nb_results[:4]
    nopc, nopr, nopminr, nopmaxr = nop_results[:4]

    theoretical_rates = 1.0 / (HALFTIME * numpy.sqrt(cooperativities))
    errors = numpy.array(numpy.array(rates) - numpy.array(min_rates)) / theoretical_rates
    rates = numpy.array(rates) / theoretical_rates

    nberrors = numpy.array(numpy.array(nbr) - numpy.array(nb_minr)) / theoretical_rates
    nbrates = numpy.array(nbr) / theoretical_rates

    noperrors = numpy.array(numpy.array(nopr) - numpy.array(nopminr)) / theoretical_rates
    noprates = numpy.array(nopr) / theoretical_rates

    with contexts.subplot(figure, (2, 1, 1), title='A',
#            x_label=r'Pi Dissociation Cooperativity, $\rho_d$',
            y_label=r'$r_d$ [Simulation / Theory]',
            logscale_x=True,
            ) as axes:
        axes.axvline(RHO_CRIT, 0, 1, linestyle='--', color='g', linewidth=0.5)

        # With enhanced BE dissociation rate
        contexts.plot(axes, 'errorbar', cooperativities,
                rates, errors, fmt='k.')

        # Without enhanced BE dissociation rate
        contexts.plot(axes, 'errorbar', cooperativities,
                nbrates, nberrors, fmt='b.')

        # No pointed end kinetics
        contexts.plot(axes, 'errorbar', cooperativities,
                noprates, noperrors, fmt='g.')

        contexts.plot(axes, 'plot', cooperativities,
                [1 for c in cooperativities], 'r-', linewidth=0.5)
        axes.set_xlim([0.1, 10**12])

        axes.set_xticks([1, 100, 10000, 1000000,
            100000000, 10000000000])
        

        axes.set_ylim([0, 1.2])

def non_be_quality(figure):
    results = data.load_data('results/melki_cooperative_fit.dat')
    (cooperativities, rates, min_rates, max_rates, rate_pe,
            chi2, min_chi2, max_chi2, chi2_pe) = results
    nb_results = data.load_data('results/melki_non_be_coop_fit.dat')
    (nbc, nbr, nbminr, nbmaxr, nbrpe, nbchi2, nbminc2,
            nbmaxc2, nbcpe) = nb_results
    nop_results = data.load_data('results/melki_no_pointed_coop_fit.dat')
    (nbc, nopr, junk, junk, jukn,
            nopc2, nopminc2, nopmaxc2, junk) = nop_results

    v_results = data.load_data('results/melki_vectorial_fit.dat')
    (v_rate, junk, junk, junk,
            v_chi2, v_min_chi2, v_max_chi2, junk) = zip(*v_results)[0]
    v_nb_results = data.load_data('results/melki_non_be_vec_fit.dat')
    (v_nbr, v_nbminr, v_nbmaxr, v_nbrpe, v_nbchi2, v_nbminc2,
            v_nbmaxc2, v_nbcpe) = zip(*v_nb_results)[0]

    with contexts.subplot(figure, (2, 1, 2), title='B',
            x_label=r'Pi Dissociation Cooperativity, $\rho_d$',
            y_label=r'$\chi^2$ Comparison To Data',
            logscale_x=True) as axes:
        axes.fill_between([0.1, 1.0e12],
                [v_min_chi2, v_min_chi2],
                v_max_chi2, color='#AAAAAA')
        axes.fill_between([0.1, 1.0e12],
                [v_nbminc2, v_nbminc2],
                v_nbmaxc2, color='#CCCCFF')
        axes.axhline(v_chi2, 0, 1, linestyle=':', color='k')
        axes.axhline(v_nbchi2, 0, 1, linestyle=':', color='b')
        axes.axvline(RHO_CRIT, 0, 1, linestyle='--', color='g', linewidth=0.5)

        contexts.plot(axes, 'errorbar', cooperativities,
                chi2, [c - m for c, m in zip(chi2, min_chi2)],
                fmt='k.')

        contexts.plot(axes, 'errorbar', cooperativities,
                nbchi2, [c - m for c, m in zip(nbchi2, nbminc2)],
                fmt='b.')

        contexts.plot(axes, 'errorbar', cooperativities,
                nopc2, [c - m for c, m in zip(nopc2, nopminc2)],
                fmt='g.')

        axes.set_xlim([0.1, 10**12])
        axes.set_ylim([0, 14])

        axes.set_xticks([1, 100, 10000, 1000000,
            100000000, 10000000000])

if '__main__' == __name__:
    main()
