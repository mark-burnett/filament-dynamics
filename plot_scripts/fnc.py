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

from actin_dynamics.io import data

from plot_scripts import contexts
from plot_scripts import settings

LINETYPES = ['r', 'g', 'c', 'b', 'm', 'y', 'k']

SCALE_BY_RANDOM = False


def main(filename='plots/fnc_results.eps'):
    with contexts.complex_figure(filename#,
#            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2
            ) as figure:
        fnc_zoomed_out(figure)

def fnc_zoomed_out(figure):
    results = data.load_data('results/fnc_halftimes.dat')
    v_results = data.load_data('results/vectorial_fnc_halftimes.dat')

    fncs, all_halftimes = results[0], results[1:]
    v_fncs, v_halftimes = v_results[0], v_results[1]

    if SCALE_BY_RANDOM:
        y_label = 'Normalized [Pi] Halftime'
        scale_value = all_halftimes[0][0]
    else:
        y_label = '[Pi] Halftime [s]'

    with contexts.subplot(figure, (1, 1, 1),
            x_label=r'Filament Number Concentration [$\mu$M]',
            y_label=y_label,
            logscale_x=True) as axes:
        for halftimes, lt in zip(all_halftimes, LINETYPES):
            if SCALE_BY_RANDOM:
                scaled_halftimes = [ht / scale_value for ht in halftimes]
            else:
                scaled_halftimes = halftimes
            contexts.plot(axes, 'plot', fncs, scaled_halftimes, lt)

        if SCALE_BY_RANDOM:
            v_scaled_halftimes = [ht / scale_value for ht in v_halftimes]
        else:
            v_scaled_halftimes = v_halftimes
        contexts.plot(axes, 'plot', v_fncs, v_scaled_halftimes, 'k')

        axes.set_xlim(0.001, 0.1)

if '__main__' == __name__:
    main()
