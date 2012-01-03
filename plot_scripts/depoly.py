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

THIN_LINE = 0.3

def main(filename='plots/depoly_timecourses.eps'):
    with contexts.complex_figure(filename,
#            height=settings.DOUBLE_COLUMN_DEFAULT_HEIGHT_CM,
#            width=settings.DOUBLE_COLUMN_DEFAULT_WIDTH_CM) as figure:
            width=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2,
            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2) as figure:
        random_vectorial_timecourse(figure)
    #    tip_filaments(figure)
        tip_fit(figure)
        rate_fit(figure)
        cooperative_timecourse(figure)

def tip_fit(figure):
    best_tc = data.load_data('results/depoly_timecourse.dat')

    times, values = numpy.array(best_tc[0]), numpy.array(best_tc[1])
    times -= 300
    values *= 0.0027

    expt = data.load_data(
            'experimental_data/jegou_2011/sample_filament_timecourse.dat')
    etimes, evals = numpy.array(expt[0]), expt[1]

#    with contexts.basic_figure('plots/depoly_tip_fit_timecourse.eps',
    with contexts.subplot(figure, (2, 2, 2), title='B'
#            x_label='Time [s]',
#            y_label=r'Filament Length [$\mu$m]'
            ) as axes:
        contexts.plot(axes, 'plot', times, values, 'r-')
        contexts.plot(axes, 'plot', etimes, evals, 'k-')

        axes.set_xlim(0, 1000)
        axes.set_ylim(0, 15)

def rate_fit(figure):
    random_results = data.load_data('results/depoly_fit_release_rate.dat')

    expt = data.load_data(
            'experimental_data/jegou_2011/sample_filament_timecourse.dat')

    rtimes, rvalues = numpy.array(random_results[0]), random_results[1:]

    etimes, evals = numpy.array(expt[0]), expt[1]

    rtimes -= 300

#    with contexts.basic_figure('plots/depoly_tip_filaments.eps',
    with contexts.subplot(figure, (2, 2, 3), title='C',
            x_label='Time [s]',
            y_label=r'Filament Length [$\mu$m]') as axes:
        for y in rvalues:
            y = numpy.array(y)
            y *= 0.0027
            contexts.plot(axes, 'plot', rtimes, y, '-', color='#FF8080',
                    linewidth=THIN_LINE)

        contexts.plot(axes, 'plot', etimes, evals, 'k', linewidth=0.7)
        axes.set_ylim(0, 15)
        axes.set_xlim(0, 1000)

def tip_filaments():
    random_results = data.load_data('results/depolymerization_timecourses.dat')

    expt = data.load_data(
            'experimental_data/jegou_2011/sample_filament_timecourse.dat')

    rtimes, rvalues = numpy.array(random_results[0]), random_results[1:]

    etimes, evals = numpy.array(expt[0]), expt[1]

    rtimes -= 300

#    with contexts.basic_figure('plots/depoly_tip_filaments.eps',
    with contexts.subplot(figure, (2, 2, 3), title='A',
            x_label='Time [s]',
            y_label=r'Filament Length [$\mu$m]') as axes:
        for y in rvalues:
            y = numpy.array(y)
            y *= 0.0027
            contexts.plot(axes, 'plot', rtimes, y, '-', color='#FFA0A0',
                    linewidth=THIN_LINE)

        contexts.plot(axes, 'plot', etimes, evals, 'k', linewidth=0.7)
        axes.set_ylim(0, 15)
        axes.set_xlim(0, 1000)


def random_vectorial_timecourse(figure):
    random_results = data.load_data('results/depoly_timecourse_random.dat')
    vectorial_results = data.load_data('results/depoly_timecourse_vectorial.dat')

    expt = data.load_data(
            'experimental_data/jegou_2011/sample_filament_timecourse.dat')

    rtimes, rvalues = numpy.array(random_results[0]), random_results[1:]
    vtimes, vvalues = numpy.array(vectorial_results[0]), vectorial_results[1:]

    etimes, evals = numpy.array(expt[0]), expt[1]

    rtimes -= 300
    vtimes -= 300

#    with contexts.basic_figure('plots/depoly_rv_timecourses.eps',
    with contexts.subplot(figure, (2, 2, 1), title='A',
#            x_label='Time [s]',
            y_label=r'Filament Length [$\mu$m]') as axes:
        for y in rvalues:
            y = numpy.array(y)
            y *= 0.0027
            contexts.plot(axes, 'plot', rtimes, y, '-',
                    color='#FF8080',
#                    color='#FFA0A0',
                    linewidth=THIN_LINE)

        for y in vvalues:
            y = numpy.array(y)
            y *= 0.0027
            contexts.plot(axes, 'plot', vtimes, y, '-',
                    color='#8080FF',
#                    color='#A0A0FF',
                    linewidth=THIN_LINE)

        contexts.plot(axes, 'plot', etimes, evals, 'k', linewidth=0.7)
        axes.set_ylim(0, 15)
        axes.set_xlim(0, 1000)


def cooperative_timecourse(figure):
    filament_results = data.load_data(
            'results/depoly_timecourse_rho_200000.dat')
    mean_results = data.load_data('results/depoly_mean_tc.dat')

    expt = data.load_data(
            'experimental_data/jegou_2011/sample_filament_timecourse.dat')

    ftimes, fvalues = numpy.array(filament_results[0]), filament_results[1:]
    mtimes, mvalues = (numpy.array(mean_results[0]),
            0.0027 * numpy.array(mean_results[1]))

    etimes, evals = numpy.array(expt[0]), expt[1]

    ftimes -= 300
    mtimes -= 300

#    with contexts.basic_figure('plots/depoly_coop_timecourses.eps',
    with contexts.subplot(figure, (2, 2, 4), title='D',
            x_label='Time [s]'
#            y_label=r'Filament Length [$\mu$m]'
            ) as axes:
        for y in fvalues:
            y = numpy.array(y)
            y *= 0.0027
            contexts.plot(axes, 'plot', ftimes, y, '-',
#                    color='#FF8080',
#                    color='#80FF80',
                    color='#8080FF',
                    linewidth=THIN_LINE)

        contexts.plot(axes, 'plot', etimes, evals, 'k-', linewidth=0.7)
        contexts.plot(axes, 'plot', mtimes, mvalues, 'r-', linewidth=0.7)

        axes.set_ylim(0, 15)
        axes.set_xlim(0, 1000)


if '__main__' == __name__:
    main()
