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


from plot_scripts import contexts
from plot_scripts import settings

def main():
    constraint_plot()


CONSTRAINTS = [
        (1, 100, 'Melki 1996'), # Melki visual inspection
        (10000, 1000000, 'Jegou 2011'), # Jegou/Carlier depoly sample filament
        (1, 1000000, 'Carlier 1986') # Carlier86 FNC variation
        ]

TEXT_X = max(c[1] for c in CONSTRAINTS) * 10

def constraint_plot():
    centers = [float(a + b)/2 for (a, b, n) in CONSTRAINTS]
    widths = [float(b - a)/2 for (a, b, n) in CONSTRAINTS]
    names = [c[2] for c in CONSTRAINTS]

    with contexts.basic_figure('plots/cooperativity_constraints.eps',
            x_label=r'Pi Dissociation Cooperativity, $\rho_d$',
#            y_label=r'Pi Dissociation Rate, $r_d$ [$s^{-1}$]',
            logscale_x=True) as axes:

        contexts.plot(axes, 'errorbar',
            centers, range(1, len(centers) + 1), xerr=widths,
                fmt='k.', ms=0)

        for i, (low, high, name) in enumerate(CONSTRAINTS):
            axes.text(TEXT_X, i + 0.9, name)

        axes.set_xlim([0.1, 10**13])
        axes.set_xticks([1, 10, 100, 1000, 10000, 100000, 1000000])

        # Remove extra ticks on the right.
        axes.set_xticks([], minor=True)

        axes.set_ylim([0, len(centers) + 1])
        axes.set_yticks([])


if '__main__' == __name__:
    main()
