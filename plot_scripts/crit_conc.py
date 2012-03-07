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

def main():
#    with contexts.complex_figure('plots/critical_concentration.pdf',
    with contexts.complex_figure('plots/cc_tip.pdf',
            width=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM,
            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2) as figure:
#        crit_conc(figure)
        cc_tip(figure)
#        D(figure)


def crit_conc(figure):
    results = data.load_data('results/cc_d_cooperative.dat')
    v_results = data.load_data('results/cc_d_vectorial.dat')

    coops, ccs, ds = results
    vcc, vd = v_results[0][0], v_results[1][0]

    with contexts.subplot(figure, (2, 1, 1), title='A',
            y_label=r'Critical Concentration [$\mu$M]',
            logscale_x=True, logscale_y=False) as axes:
        contexts.plot(axes, 'plot', coops, ccs, 'k-')

        axes.axhline(vcc, 0, 1, linestyle=':', linewidth=0.5, color='k')
        axes.set_ylim(0.1, 0.2)

    with contexts.subplot(figure, (2, 1, 2), title='B',
            y_label=r'Diffusion Coefficient [mon^2/s]',
            logscale_x=True, logscale_y=False) as axes:
        contexts.plot(axes, 'plot', coops, ds, 'k-')
        axes.axhline(vd, 0, 1, linestyle=':', linewidth=0.5, color='k')

def cc_tip(figure):
    results = data.load_data('results/cc_d_tip.dat')

    pars, ccs, ds = results

    with contexts.subplot(figure, (2, 1, 1), title='A',
            y_label=r'Critical Concentration [$\mu$M]',
            logscale_x=False, logscale_y=False) as axes:
        contexts.plot(axes, 'plot', pars, ccs, 'k-')


    with contexts.subplot(figure, (2, 1, 2), title='B',
            y_label=r'Diffusion Coefficient [mon^2/s]',
            x_label=r'Barbed End Pi Dissociation Rate [s$^{-1}$]',
            logscale_x=False, logscale_y=False) as axes:
        contexts.plot(axes, 'plot', pars, ds, 'k-')



if '__main__' == __name__:
    main()
