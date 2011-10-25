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

THIN_LINE = 0.1

def main():
    depoly_timecourse()

def depoly_timecourse():
    fuji_results = data.load_data('results/depolymerization_timecourses.dat')
#    fuji_results = data.load_data('results/depoly_tc_fuji_pars.dat')
#    jegou_results = data.load_data('results/depoly_tc_jegou_pars.dat')

    expt = data.load_data(
            'experimental_data/jegou_2011/sample_filament_timecourse.dat')

    ftimes, fvalues = numpy.array(fuji_results[0]), fuji_results[1:]
#    jtimes, jvalues = numpy.array(jegou_results[0]), jegou_results[1:]
    etimes, evals = numpy.array(expt[0]), expt[1]

    ftimes -= 300
#    jtimes -= 300

    with contexts.basic_figure('plots/depoly_timecourse.eps',
            x_label='Time [s]',
            y_label=r'Filament Length [$\mu$m]') as axes:
        for y in fvalues:
            y = numpy.array(y)
            y *= 0.0027
            contexts.plot(axes, 'plot', ftimes, y, '-', color='#FFA0A0',
                    linewidth=THIN_LINE)

#        for y in jvalues:
#            y = numpy.array(y)
#            y *= 0.0027
#            contexts.plot(axes, 'plot', jtimes, y, '-', color='blue',
##                    color='#FF8080',
#                    linewidth=THIN_LINE)

        contexts.plot(axes, 'plot', etimes, evals, 'k', linewidth=0.7)
        axes.set_ylim(0, 15)
        axes.set_xlim(0, 1000)

if '__main__' == __name__:
    main()
