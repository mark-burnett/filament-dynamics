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

import numpy

from actin_dynamics.io import data

from plot_scripts import contexts
from plot_scripts import settings

LINETYPES = ['k', ':r', ':b', 'b', 'm', 'y', 'k']

SCALE_BY_RANDOM = False
RHO_CRIT = (20/0.02)**2


def main(filename='plots/fnc_lagtimes.eps'):
    with contexts.complex_figure(filename,
            width=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM,
            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2,
            ) as figure:
#        lagtime_plot(figure)
        linear_lagtime_plot(figure)
        qof_plot(figure)


def linear_lagtime_plot(figure,
        coop_linestyles=['k:', # Random
                         'r:', # XXX Consider making green
                         'b:',
                         'm:'
                         ],
        cooperative_filename='results/fnc_cooperative_lagtimes.dat',
        vectorial_filename='results/fnc_vectorial_lagtimes.dat',
        data_filename='experimental_data/carlier_1986/lagtimes.dat'):
    d_fncs, d_lagtimes = data.load_data(data_filename)
    d_norm_lagtimes = d_lagtimes[0] / numpy.array(d_lagtimes)

    coop_data = data.load_data(cooperative_filename)
    coop_fncs, coop_lagtimes = coop_data[0], coop_data[1:]
    coop_fncs = numpy.array(coop_fncs) * 1000

    v_fncs, v_lagtimes = data.load_data(vectorial_filename)
    v_fncs = numpy.array(v_fncs) * 1000
    # index 0 is at fnc = 1.1 nM
    v_lagtimes = v_lagtimes[0] / numpy.array(v_lagtimes)

    th_fncs = numpy.linspace(1, 20, 100)
    v_theory = th_fncs / 1.1

    r_theory = numpy.ones(len(th_fncs))

    with contexts.subplot(figure, (2, 1, 1), title='A',
            x_label=r'Filament Number Concentration [nM]',
            y_label=r'(Lag Time)$^{-1}$ [AU]') as axes:
        # Cooperative simulations
        for lagtimes, linestyle in zip(coop_lagtimes, coop_linestyles):
            # index 0 is at fnc = 1.1 nM
            y = lagtimes[0] / numpy.array(lagtimes)
            axes.plot(coop_fncs, y, linestyle)

        # Vectorial simulations
        axes.plot(v_fncs, v_lagtimes, 'k:')

        # Vectorial theory
        axes.plot(th_fncs, v_theory, 'k-', linewidth=0.5)

        # Random theory
        axes.plot(th_fncs, r_theory, 'k-', linewidth=0.5)
        
        # Carlier 1986 data
        axes.plot(d_fncs, d_norm_lagtimes, 'ko')

        axes.set_xlim([0, 22])
        x_ticks = [1.1, 5, 10, 15, 20]
        axes.set_xticks(x_ticks)
        axes.set_xticklabels(map(str, x_ticks))


def qof_plot(figure):
    coop_qof = data.load_data('results/fnc_cooperative_qof.dat')
    vec_qof = data.load_data('results/fnc_vectorial_qof.dat')
    coops, qof, min_qof, max_qof, pct_err = coop_qof
    err = [m - q for m, q in zip(max_qof, qof)]
    with contexts.subplot(figure, (2, 1, 2), title='B',
            x_label=r'Phosphate Dissociation Cooperativity, $\rho_d$',
            y_label=r'Lag-time Quality of Fit, $\chi^2$',
            logscale_x=True, logscale_y=False) as axes:
        axes.fill_between([0.1, 1.0e12],
                [vec_qof[1][0], vec_qof[1][0]],
                vec_qof[2][0],
                color='#CCCCFF')
        axes.axhline(0, 0, 1, color='k', linestyle='-', linewidth=0.5)
        axes.axhline(vec_qof[0], 0, 1, color='b', linestyle=':')
        axes.axvline(RHO_CRIT, 0, 1, color='g', linestyle='--', linewidth=0.5)

        axes.errorbar(coops, qof, err, fmt='k.')

        axes.set_ylim([-5, None])
        axes.set_xlim([0.1, 10**12])
        axes.set_xticks([1, 100, 10000, 1000000,
            100000000, 10000000000])

if '__main__' == __name__:
    main()
