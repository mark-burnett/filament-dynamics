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
import scipy.interpolate

#import pylab

from actin_dynamics.io import data

from plot_scripts import contexts
from plot_scripts import settings

def main():
    constraint_plot()

def my_spline(x, y, newx):
    knots = scipy.interpolate.splmake(x, y, order=4, kind='smoothest')
    return scipy.interpolate.spleval(knots, newx)

def constraint_plot():
    MELKI_THRESHOLD = 4.5
    FNC_THRESHOLD = 7.5
    DEPOLY_THRESHOLD = 3

    melki_constraints = data.load_data('results/melki_cooperative_fit.dat')
    fnc_constraints = data.load_data('results/fnc_cooperative_qof.dat')
    depoly_constraints = data.load_data('results/depoly_cooperative_qof.dat')


    mrho, mchi = melki_constraints[0], melki_constraints[5]
    frho, fchi = fnc_constraints[0], fnc_constraints[1]
    drho, dchi = depoly_constraints[0], depoly_constraints[1]

    mrho = numpy.array(mrho)
    mchi = numpy.array(mchi) / MELKI_THRESHOLD
    frho = numpy.array(frho)
    fchi = numpy.array(fchi) / FNC_THRESHOLD
    drho = numpy.array(drho)
    dchi = numpy.array(dchi) / DEPOLY_THRESHOLD

    lx = numpy.linspace(0, 10, 101)

    lmr = numpy.log10(mrho)
    lfr = numpy.log10(frho)
    ldr = numpy.log10(drho)

    m_inter = my_spline(lmr, mchi, lx)
    f_inter = my_spline(lfr, fchi, lx)
    d_inter = my_spline(ldr, dchi, lx)

#    m_inter = scipy.interpolate.UnivariateSpline(lmr, mchi, k=3)(lx)
#    f_inter = scipy.interpolate.UnivariateSpline(lfr, fchi, k=3)(lx)
#    d_inter = scipy.interpolate.UnivariateSpline(ldr, dchi, k=3)(lx)

#    m_inter = scipy.interpolate.InterpolatedUnivariateSpline(lmr, mchi, k=4)(lx)
#    f_inter = scipy.interpolate.InterpolatedUnivariateSpline(lfr, fchi, k=4)(lx)
#    d_inter = scipy.interpolate.InterpolatedUnivariateSpline(ldr, dchi, k=4)(lx)

#    m_inter = numpy.exp(scipy.interpolate.InterpolatedUnivariateSpline(lmr,
#        numpy.log(mchi), k=4)(lx))
#    f_inter = numpy.exp(scipy.interpolate.InterpolatedUnivariateSpline(lfr,
#        numpy.log(fchi), k=4)(lx))
#    d_inter = numpy.exp(scipy.interpolate.InterpolatedUnivariateSpline(ldr,
#        numpy.log(dchi), k=4)(lx))

    with contexts.basic_figure('plots/cooperativity_constraints.pdf',
            x_label=r'Dissociation Cooperativity, $\rho_d$',
            y_label=r'Scaled Quality of Fit',
            logscale_x=False) as axes:

    #    pylab.ioff()
    #    figure = pylab.figure()
    #    axes = pylab.gca()
        axes.fill_between(lx, m_inter, 1, where=m_inter <= 1,
                    color='r', alpha=0.6,
    #            color='#BB6666',
                interpolate=True)
        axes.fill_between(lx, f_inter, 1, where=f_inter <= 1,
                    color='b', alpha=0.6,
    #            color='#6666BB',
                interpolate=True)
        axes.fill_between(lx, d_inter, 1, where=d_inter <= 1,
                    color='y', alpha=0.6,
    #            color='#6666BB',
                interpolate=True)


        axes.plot(lx, m_inter, 'k-')
        axes.plot(lx, f_inter, 'k--')
        axes.plot(lx, d_inter, 'k-.')



        axes.axhline(1, 0, 1, color='k')
        # XXX Optional vertical line
#        axes.axvline(0, 0, 1.0/6, color='k')

        axes.set_xlim([-1, 11])
        axes.set_xticks([0, 2, 4, 6, 8, 10])
        axes.set_xticklabels([1, r'$10^2$', r'$10^4$', r'$10^6$',
            r'$10^8$', r'$10^{10}$'])

        axes.set_ylim([0, None])
#        pylab.show()


if '__main__' == __name__:
    main()
