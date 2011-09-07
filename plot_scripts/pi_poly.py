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

TIMECOURSE_HALFTIME = 406
HALF_CONCENTRATION = 1008

def main(filename='plots/pi_saturation.eps'):
    with contexts.complex_figure(filename,
#            width=settings.DOUBLE_COLUMN_DEFAULT_WIDTH_CM,
#            height=settings.DOUBLE_COLUMN_DEFAULT_HEIGHT_CM
            width=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2,
            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2) as figure:
        timecourse_plot(figure)
        asymptotic_plot(figure)
        halftime_plot(figure)
        cooperativity_plot(figure)


# XXX convert to minutes
# XXX add [Pi*]
def timecourse_plot(figure, xmax=3600, ymax=35):
    timecourses = data.load_data('results/pi_saturation_timecourse.dat')

    with contexts.subplot(figure, (2, 2, 1), title='A',
            x_label='Time [s]',
            y_label=r'Concentrations [$\mu$M]') as axes:
        # factin
        contexts.plot(axes, 'plot', timecourses[0], timecourses[1], 'b-.')
        # adp-pi
        contexts.plot(axes, 'plot', timecourses[0], timecourses[3], 'g-')
        # pi
        contexts.plot(axes, 'plot', timecourses[0], timecourses[5], 'r-')

        axes.set_xlim(0, xmax)
        axes.set_ylim(0, ymax)

        # Lines to highlight halftime
        axes.axhline(15, 0, float(TIMECOURSE_HALFTIME)/xmax,
                linestyle=':', linewidth=0.5, color='k')
        axes.axvline(TIMECOURSE_HALFTIME, 0, 15.0 / 35,
                linestyle=':', linewidth=0.5, color='k')

        # Halftime label with arrow
        axes.annotate('halftime', xy=(TIMECOURSE_HALFTIME, 0.05),
                xytext=(TIMECOURSE_HALFTIME + 200, 5),
                arrowprops={'facecolor': 'black',
                    'arrowstyle': '->'},
                size=settings.SMALL_FONT_SIZE)

        # Curve labels
        axes.text(0.5 * xmax, 30.5, '[F-actin]',
                horizontalalignment='center', verticalalignment='bottom',
                size=settings.SMALL_FONT_SIZE)
        axes.text(600, 20.5, '[ADP-Pi-actin]',
                horizontalalignment='right', verticalalignment='bottom',
                size=settings.SMALL_FONT_SIZE)


def asymptotic_plot(figure):
    results = data.load_data('results/asymptotic_adppi_v_pi.dat')
    pis, fractions = results[0], results[1:]

    with contexts.subplot(figure, (2, 2, 2), title='C',
            x_label=r'Pi Concentration [$\mu$M]',
            y_label=r'Asymptotic Fraction [F-ADP-Pi-actin]',
            logscale_x=True) as axes:
#        for frac in fractions:
#            contexts.plot(axes, 'plot', pis, frac)
        contexts.plot(axes, 'plot', pis, fractions[0], 'b')

        axes.set_ylim(0, 1)

        axes.axhline(0.5, 0, 1, linestyle='-', linewidth=0.5, color='k')
        axes.axvline(HALF_CONCENTRATION, 0, 0.5,
                linestyle=':', linewidth=0.5, color='k')

        axes.annotate(r'$c^*$', xy=(HALF_CONCENTRATION, 0.001),
                xytext=(HALF_CONCENTRATION + 2000, 0.15),
                arrowprops={'facecolor': 'black',
                    'arrowstyle': '->'},
                size=settings.SMALL_FONT_SIZE)

        axes.text(4000, 0.8, r'$\rho_d =\,1$',
                horizontalalignment='right', # verticalalignment='bottom',
                size=settings.SMALL_FONT_SIZE)



def halftime_plot(figure):
    pass


def cooperativity_plot(figure):
    x, y = data.load_data('results/rho_v_pi.dat')
    with contexts.subplot(figure, (2, 2, 4), title='D',
#            x_label=r'Asymptotic Fraction [F-ADP-Pi-actin]',
            x_label=r'[Pi]$_{\frac{1}{2}}$ [$\mu$M]',
            y_label=r'Pi Dissociation Cooperativity, $\rho_d$',
            logscale_x=True, logscale_y=True) as axes:
        contexts.plot(axes, 'plot', x, y, 'k')


if '__main__' == __name__:
    main()
