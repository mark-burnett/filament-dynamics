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

THIN_LINE = 0.2

def main():
    depoly_timecourse()

def depoly_timecourse():
    sim_results = data.load_data('results/depolymerization_timecourses.dat')

    times, values = sim_results[0], sim_results[1:]

    with contexts.basic_figure('plots/depoly_timecourse.eps',
            x_label='Time [s]',
            y_label=r'Filament Length [$\mu$M]') as axes:
        for y in values:
            y = numpy.array(y)
            y *= 0.0027
            contexts.plot(axes, 'plot', times, y, '-', color='#FF8080',
                    linewidth=THIN_LINE)
        axes.set_xlim(600, 1600)

if '__main__' == __name__:
    main()
