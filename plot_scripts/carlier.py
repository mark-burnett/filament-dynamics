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

import pprint

import numpy
import scipy

from actin_dynamics.io import data
from actin_dynamics.numerical import meshes

from plot_scripts import contexts
from plot_scripts import settings

ACTIN_CONCENTRATION = 40

def main():
    carlier_timecourses()

def carlier_timecourses():
    _timecourse(0.0011,
            'experimental_data/carlier_1986/factin_tc_fnc_1.1.dat',
            'experimental_data/carlier_1986/adppi_tc_fnc_1.1.dat',
            'results/carlier_timecourses_1.1.dat',
            'plots/carlier_86_tc_1.1.pdf')

    _timecourse(0.02,
            'experimental_data/carlier_1986/factin_tc_fnc_20.dat',
            'experimental_data/carlier_1986/adppi_tc_fnc_20.dat',
            'results/carlier_timecourses_20.dat',
            'plots/carlier_86_tc_20.pdf')

def _timecourse(fnc, f_filename, p_filename, sim_filename,
        output_filename):
    ftimes, fdata = data.load_data(f_filename)
    ptimes, pdata = data.load_data(p_filename)
    sim_results = data.load_data(sim_filename)

    stimes = numpy.array(sim_results[0])
    slengths = numpy.array(sim_results[1])
    sadppi = numpy.array(sim_results[3])

    stimes /= 60
    slengths *= fnc / ACTIN_CONCENTRATION
    sadppi *= fnc / ACTIN_CONCENTRATION

    with contexts.basic_figure(output_filename,
            x_label='Time [min]',
            y_label='Polymer Fraction') as axes:
        contexts.plot(axes, 'plot', ftimes, fdata, 'k.')
        contexts.plot(axes, 'plot', ptimes, pdata, 'r.')

        contexts.plot(axes, 'plot', stimes, slengths, 'k-')
        contexts.plot(axes, 'plot', stimes, sadppi, 'r-')

        axes.set_xlim(0, 35)


if '__main__' == __name__:
    main()
