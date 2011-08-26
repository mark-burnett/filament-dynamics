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
import scipy

from actin_dynamics.io import data
from actin_dynamics.numerical import meshes

from plot_scripts import contexts
from plot_scripts import settings

LINETYPES = ['r', 'g', 'c', 'b', 'm', 'y', 'k']

X_LABEL_MARGIN = -0.1
X_LABEL_PADDING = 0.075

def main(filename='plots/copoly_results.eps'):
    with contexts.figure(filename,
            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2) as figure:
        copoly_timecourse_plot(figure)
        copoly_halftime_plot(figure)

def copoly_timecourse_plot(figure, xmax=1000, ymax=35):
    timecourses = data.load_data('results/copoly_timecourse.dat')

    with contexts.subplot(figure, (2, 1, 1), title='A',
            x_label='Time [s]',
            y_label=r'Concentrations [$\mu$M]') as axes:
        # factin
        contexts.plot(axes, 'plot', timecourses[0], timecourses[1], 'b-.')
        # pi
        contexts.plot(axes, 'plot', timecourses[0], timecourses[3], 'g-')

        axes.set_xlim(0, xmax)
        axes.set_ylim(0, ymax)

        axes.axhline(15, 0, 1, linestyle=':', linewidth=1, color='k')
        axes.axvline(403, 0, 15.0 / 35, linestyle=':', linewidth=1, color='k')

def copoly_halftime_plot(figure):
    adp_halftimes = data.load_data('results/adp_copoly_halftimes.dat')
    nh_halftimes = data.load_data('results/nh_copoly_halftimes.dat')

    fractions, combined_data = _combine_data(adp_halftimes, nh_halftimes)

    with contexts.subplot(figure, (2, 1, 2), title='B',
#            x_label='',
#            x_label='Contaminant Fraction [%]',
            y_label=r'Halftime [s]',
            logscale_y=True) as axes:
        for local_data, lt, in zip(combined_data, LINETYPES):
            contexts.plot(axes, 'plot', fractions, local_data, lt)

        new_x_tick_labels = [10, 5, 0, 5, 10]

        axes.set_xticks([-10, -5, 0, 5, 10])
        axes.set_xticklabels(new_x_tick_labels)

        axes.text(X_LABEL_PADDING, X_LABEL_MARGIN, 'ADP-actin %',
                verticalalignment='top', horizontalalignment='left',
                transform=axes.transAxes)
        axes.text(1 - X_LABEL_PADDING, X_LABEL_MARGIN, 'NH-actin %',
                verticalalignment='top', horizontalalignment='right',
                transform=axes.transAxes)

#        axes.set_xlim([0.1, 10000000])
#        axes.set_ylim([1e-5, 0.01])


def _combine_data(adp_halftimes, nh_halftimes):
    adp_fractions = adp_halftimes[0]
    nh_fractions = nh_halftimes[0]

    adp_data = adp_halftimes[1:]
    nh_data = nh_halftimes[1:]

    all_fractions = [-f for f in reversed(adp_fractions)]
    all_fractions.extend(nh_fractions)

    all_fractions = [100 * f for f in all_fractions]

    all_data = []
    for ad, nh in zip(adp_data, nh_data):
        this_data = list(reversed(ad))
        this_data.extend(nh)
        all_data.append(this_data)

    return all_fractions, all_data



if '__main__' == __name__:
    main()

