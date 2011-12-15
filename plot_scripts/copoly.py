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

from plot_scripts import contexts
from plot_scripts import settings

LINETYPES = ['k', 'r', 'g', 'c', 'b', 'm', 'y']

X_LABEL_MARGIN = -0.1
X_LABEL_PADDING = 0.075

TIMECOURSE_HALFTIME = 388
HT_ARROW_X_OFFSET = 25

INCREASING_RHO_TEXT = r'''increasing
$\rho_d$'''

def main(filename='plots/copoly_results.eps'):
#    copoly_adp_only(filename)
#    copoly_halftime_plot(filename)
    with contexts.complex_figure(filename,
            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2) as figure:
        copoly_timecourse_plot(figure)
        copoly_adp_only(figure)
#        copoly_halftime_plot(figure)

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

        # Lines to highlight halftime
        axes.axhline(15, 0, 1, linestyle='-', linewidth=0.5, color='k')
        axes.axvline(TIMECOURSE_HALFTIME, 0, 15.0 / 35,
                linestyle=':', linewidth=0.5, color='k')

        # Halftime label with arrow
#        axes.annotate('halftime', xy=(TIMECOURSE_HALFTIME, 0.05),
        axes.annotate(r'$t_{\frac{1}{2}}$', xy=(TIMECOURSE_HALFTIME, 0.05),
                xytext=(TIMECOURSE_HALFTIME + 200, 5),
                arrowprops={'facecolor': 'black',
                    'arrowstyle': '->'},
                size=settings.SMALL_FONT_SIZE)

        # Curve labels
        axes.text(0.5 * xmax, 30.5, '[F-actin]',
                horizontalalignment='center', verticalalignment='bottom',
                size=settings.SMALL_FONT_SIZE)
        axes.text(600, 20.5, '[Pi]',
                horizontalalignment='right', verticalalignment='bottom',
                size=settings.SMALL_FONT_SIZE)

def copoly_adp_only(figure):
    adp_halftimes = data.load_data('results/adp_copoly_halftimes.dat')
    adp_v_halftimes = data.load_data('results/adp_copoly_halftimes_vectorial.dat')

    fractions, halftimes = adp_halftimes[0], adp_halftimes[1:]
    v_fractions, v_halftimes = adp_v_halftimes[0], adp_v_halftimes[1]

    with contexts.subplot(figure, (2, 1, 2), title='B',
            y_label=r'[Pi] Halftime [s]',
            x_label=r'% ADP-actin') as axes:
        for ht, lt, in zip(halftimes, LINETYPES):
            contexts.plot(axes, 'plot', fractions, ht, lt)

        contexts.plot(axes, 'plot', v_fractions, v_halftimes, 'k-')

        new_x_tick_labels = [0, 10, 20, 30, 40, 50]

        axes.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
        axes.set_xticklabels(new_x_tick_labels)

        axes.set_ylim(0, 450)


#def copoly_halftime_plot(figure):
def copoly_halftime_plot(filename):
    adp_halftimes = data.load_data('results/adp_copoly_halftimes.dat')
    nh_halftimes = data.load_data('results/nh_copoly_halftimes.dat')

    adp_v_halftimes = data.load_data('results/adp_copoly_halftimes_vectorial.dat')
    nh_v_halftimes = data.load_data('results/nh_copoly_halftimes_vectorial.dat')

    fractions, combined_data = _combine_data(adp_halftimes, nh_halftimes)
    vfractions, vcombined_data = _combine_data(adp_v_halftimes, nh_v_halftimes)


    with contexts.basic_figure(filename,
            y_label=r'Halftime [s]',
            logscale_y=True) as axes:
        for local_data, lt, in zip(combined_data, LINETYPES):
            contexts.plot(axes, 'plot', fractions, local_data, lt)

        for vld in vcombined_data:
            contexts.plot(axes, 'plot', vfractions, vld, 'k-')

#        new_x_tick_labels = [10, 5, 0, 5, 10]
#
#        axes.set_xticks([-10, -5, 0, 5, 10])

        new_x_tick_labels = [50, 40, 30, 20, 10, 0, 10]

        axes.set_xticks([-50, -40, -30, -20, -10, 0, 10])
        axes.set_xticklabels(new_x_tick_labels)

        axes.set_ylim(10, 10**5)

        axes.text(X_LABEL_PADDING, X_LABEL_MARGIN, 'ADP-actin [%]',
                verticalalignment='top', horizontalalignment='left',
                transform=axes.transAxes)
        axes.text(1 - X_LABEL_PADDING, X_LABEL_MARGIN, 'NH-actin [%]',
                verticalalignment='top', horizontalalignment='right',
                transform=axes.transAxes)

        # \rho_d arrows
        axes.annotate(INCREASING_RHO_TEXT,
                xy=(-HT_ARROW_X_OFFSET, TIMECOURSE_HALFTIME),
                xytext=(-HT_ARROW_X_OFFSET, 6e3),
                arrowprops={'facecolor': 'black',
                    'arrowstyle': '->'},
                horizontalalignment='center',
                verticalalignment='top',
                size=settings.SMALL_FONT_SIZE)

        axes.annotate(INCREASING_RHO_TEXT,
                xy=(HT_ARROW_X_OFFSET, TIMECOURSE_HALFTIME),
                xytext=(HT_ARROW_X_OFFSET, 17),
                arrowprops={'facecolor': 'black',
                    'arrowstyle': '->'},
                horizontalalignment='center',
                verticalalignment='bottom',
                size=settings.SMALL_FONT_SIZE)

        axes.axvline(0, 0, 1, linestyle=':', linewidth=0.5, color='k')


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
