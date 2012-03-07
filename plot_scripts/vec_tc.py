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

HALFTIME = 433
#RHO_CRIT = 69444444
RHO_CRIT = (15/0.00167)**2

MELKI_ERROR = 0.1

def main():
    with contexts.complex_figure('plots/melki_vc_tc_comp.pdf',
            width=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM,
            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM) as figure:
        vec_tcs(figure)



def vec_tcs(figure):
    data_f_times, data_f = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/factin_concentration.dat')
    data_p_times, data_p = data.load_data(
            'experimental_data/melki_fievez_carlier_1996/phosphate_concentration.dat')
    data_p = numpy.array(data_p)

    sim_p = data.load_data('results/melki_timecourses_p.dat')
    sp_times, sp_vals = sim_p[0], sim_p[1]

    nbesim_p = data.load_data('results/melki_nonbe_tc_p.dat')

    colors = ['b', 'g', 'r', 'orange']
    labels = ['Vectorial', 'Random', r'$\rho_d = 10^4$', r'$\rho_d = 10^8$']

    with contexts.subplot(figure, (1, 1, 1),
            x_label=r'Time [s]',
            y_label=r'Concentrations [$\mu$M]') as axes:
        axes.fill_between(data_p_times,
                data_p * (1 - MELKI_ERROR), data_p * (1 + MELKI_ERROR),
                color='#CCCCCC')
        axes.plot(data_f_times, data_f, 'k--')
        axes.plot(data_p_times, data_p, 'k-', label='Data')

        # BE included
        axes.plot(sp_times, sp_vals, color='b', linestyle='-', label='BE')
        # Non-BE
        axes.plot(nbesim_p[0], nbesim_p[1], color='r', linestyle='-', label='Non-BE')

        axes.set_ylim([0, 35])
        axes.set_xlim([0, 2500])

        axes.legend(loc=4)


if '__main__' == __name__:
    main()
