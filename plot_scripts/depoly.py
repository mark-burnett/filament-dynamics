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

def main():
    tip_filaments()
#    tip_fit()
    random_vectorial_timecourse()
    cooperative_timecourse()

def tip_fit():
    best_tc = data.load_data('results/depoly_timecourse.dat')

    times, values = numpy.array(best_tc[0]), numpy.array(best_tc[1])
    times -= 300
    values *= 0.0027

    expt = data.load_data(
            'experimental_data/jegou_2011/sample_filament_timecourse.dat')
    etimes, evals = numpy.array(expt[0]), expt[1]

    with contexts.basic_figure('plots/depoly_tip_fit_timecourse.eps',
            x_label='Time [s]',
            y_label=r'Filament Length [$\mu$m]') as axes:
        contexts.plot(axes, 'plot', times, values, 'r-')
        contexts.plot(axes, 'plot', etimes, evals, 'k-')

        axes.set_xlim(0, 1000)
        axes.set_ylim(0, 15)

def tip_filaments():
    random_results = data.load_data('results/depolymerization_timecourses.dat')

    expt = data.load_data(
            'experimental_data/jegou_2011/sample_filament_timecourse.dat')

    rtimes, rvalues = numpy.array(random_results[0]), random_results[1:]

    etimes, evals = numpy.array(expt[0]), expt[1]

    rtimes -= 300

    with contexts.basic_figure('plots/depoly_tip_filaments.eps',
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


def random_vectorial_timecourse():
    random_results = data.load_data('results/depoly_timecourse_random.dat')
    vectorial_results = data.load_data('results/depoly_timecourse_vectorial.dat')

    expt = data.load_data(
            'experimental_data/jegou_2011/sample_filament_timecourse.dat')

    rtimes, rvalues = numpy.array(random_results[0]), random_results[1:]
    vtimes, vvalues = numpy.array(vectorial_results[0]), vectorial_results[1:]

    etimes, evals = numpy.array(expt[0]), expt[1]

    rtimes -= 300
    vtimes -= 300

    with contexts.basic_figure('plots/depoly_rv_timecourses.eps',
            x_label='Time [s]',
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


def cooperative_timecourse():
    random_results = data.load_data('results/depoly_timecourse_rho_200000.dat')

    expt = data.load_data(
            'experimental_data/jegou_2011/sample_filament_timecourse.dat')

    rtimes, rvalues = numpy.array(random_results[0]), random_results[1:]

    etimes, evals = numpy.array(expt[0]), expt[1]

    rtimes -= 300

    with contexts.basic_figure('plots/depoly_coop_timecourses.eps',
            x_label='Time [s]',
            y_label=r'Filament Length [$\mu$m]') as axes:
        for y in rvalues:
            y = numpy.array(y)
            y *= 0.0027
            contexts.plot(axes, 'plot', rtimes, y, '-',
                    color='#FF8080',
#                    color='#80FF80',
                    linewidth=THIN_LINE)

        contexts.plot(axes, 'plot', etimes, evals, 'k', linewidth=0.7)
        axes.set_ylim(0, 15)
        axes.set_xlim(0, 1000)


if '__main__' == __name__:
    main()
