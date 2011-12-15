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


def main(filename='plots/fnc_lagtimes.eps'):
    with contexts.complex_figure(filename#,
#            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2
            ) as figure:
        fnc_zoomed_out(figure)

#    with contexts.complex_figure('plots/fnc_peak_times.eps'#,
#            ) as figure:
#        fnc_zoomed_out(figure, y_label='[F-ADP-Pi-actin] Peak Time [s]',
#                cooperative_filename='results/fnc_adppi_peak_times_cooperative.dat',
#                vectorial_filename='results/fnc_adppi_peak_times_vectorial.dat')
#
#    with contexts.complex_figure('plots/fnc_peak_values.eps'#,
#            ) as figure:
#        fnc_zoomed_out(figure, scale_by_x=True,
#                y_label=r'[F-ADP-Pi-actin] Peak Values [$\mu$M]',
#                cooperative_filename='results/fnc_adppi_peak_values_cooperative.dat',
#                vectorial_filename='results/fnc_adppi_peak_values_vectorial.dat')

def fnc_zoomed_out(figure, y_label='Renormalized [Pi] Lag Time [AU]',
        pi_cooperative_filename='results/fnc_pi_halftimes_cooperative.dat',
        pi_vectorial_filename='results/fnc_pi_halftimes_vectorial.dat',
        f_cooperative_filename='results/fnc_f_halftimes_cooperative.dat',
        f_vectorial_filename='results/fnc_f_halftimes_vectorial.dat',
        lagtime_data_filename='experimental_data/carlier_1986/lagtimes.dat'):
    pi_results = data.load_data(pi_cooperative_filename)
    pi_v_results = data.load_data(pi_vectorial_filename)

    f_results = data.load_data(f_cooperative_filename)
    f_v_results = data.load_data(f_vectorial_filename)

    lagtime_data = data.load_data(lagtime_data_filename)

    rescaled_lagtime_data = (lagtime_data[0],
            _rescale_by_final_value(lagtime_data[1]))


    fncs, pi_all_halftimes = pi_results[0], pi_results[1:]
    pi_v_fncs, pi_v_halftimes = pi_v_results[0], pi_v_results[1]

    fncs, f_all_halftimes = f_results[0], f_results[1:]
    f_v_fncs, f_v_halftimes = f_v_results[0], f_v_results[1]

    fncs = numpy.array(fncs) * 1000

    v_lagtimes = numpy.array(pi_v_halftimes) - numpy.array(f_v_halftimes)
    scaled_v_lagtimes = _rescale_by_final_value(v_lagtimes)

    with contexts.subplot(figure, (1, 1, 1),
            x_label=r'Filament Number Concentration [nM]',
            y_label=y_label,
            logscale_x=False) as axes:
        for pi_halftimes, f_halftimes, lt in zip(pi_all_halftimes,
                f_all_halftimes, LINETYPES):
            lagtimes = numpy.array(pi_halftimes) - numpy.array(f_halftimes)
            scaled_lagtimes = _rescale_by_final_value(lagtimes)
            contexts.plot(axes, 'plot', fncs, scaled_lagtimes, lt)

        contexts.plot(axes, 'plot', fncs, scaled_v_lagtimes, 'k')

        contexts.plot(axes, 'plot', rescaled_lagtime_data[0],
                rescaled_lagtime_data[1], 'ok')

        x_ticks = [1.1, 5, 10, 15, 20]
        axes.set_xticks(x_ticks)
        axes.set_xticklabels(map(str, x_ticks))

        axes.set_xlim(0, 22)

def _rescale_by_final_value(trace):
    final_value = trace[-1]
    new_results = numpy.array(trace) / final_value
    return new_results

if '__main__' == __name__:
    main()
