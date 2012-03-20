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
THICK_LINE = 1

def main():
    with contexts.complex_figure('plots/depoly.pdf',
            height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2,
            width=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM) as figure:
        quad_timecourses(figure)

        coop_qof(figure)


# units for location box are normalized from 0-1 for the whole figure
MARGIN = 0.05
SPACING = 0.05
V_SIZE = (0.5 - 2 * MARGIN - SPACING) / 2
H_SIZE = (1 - 2 * MARGIN - SPACING) / 2

L_SIDE = MARGIN
B_SIDE = 0.5 + MARGIN
R_SIDE = L_SIDE + H_SIZE + SPACING
T_SIDE = B_SIDE + V_SIZE + SPACING

# location box is: left, bottom, width, height
LOCATIONS = {'tl': (L_SIDE, T_SIDE, H_SIZE, V_SIZE),
             'tr': (R_SIDE, T_SIDE, H_SIZE, V_SIZE),
             'bl': (L_SIDE, B_SIDE, H_SIZE, V_SIZE),
             'br': (R_SIDE, B_SIDE, H_SIZE, V_SIZE)}

def _quad_sub(figure, title, location='tl',
        title_position=0.05):
    box = LOCATIONS[location]
    axes = figure.add_axes(box, frame_on=False)

    axes.set_xticks([])
    axes.set_yticks([])

    axes.set_title(title, x=title_position)
    return axes

def add_scale_bar(axes, scale_bar, scale_units=(r's', r'$\mu$m'),
        scale_position=(0.15, 0.15)):
    x_width, y_height = scale_bar
    x_y_frac, y_x_frac = scale_position

    ymax = float(axes.get_ylim()[1])
    xmax = float(axes.get_xlim()[1])

    x_y_pos = x_y_frac * ymax
    y_x_pos = y_x_frac * xmax

    x_min_frac = y_x_frac
    y_min_frac = x_y_frac

    x_max_frac = x_min_frac + x_width / xmax
    y_max_frac = y_min_frac + y_height / ymax

    axes.axhline(x_y_pos, x_min_frac, x_max_frac,
            color='k', linestyle='-', linewidth=1)
    axes.axvline(y_x_pos, y_min_frac, y_max_frac,
            color='k', linestyle='-', linewidth=1)

    x_units, y_units = scale_units
    x_label = '%i %s' % (x_width, x_units)
    y_label = '%i %s' % (y_height, y_units)

    offset = 0.025
    x_text_pos = (x_width/xmax/2 + x_min_frac) * xmax
    axes.text(x_text_pos, (x_y_frac - offset) * ymax, x_label,
            horizontalalignment='center',
            verticalalignment='top',
            fontsize=settings.TINY_FONT_SIZE
            )
    y_text_pos = (y_height/ymax/2 + y_min_frac) * ymax
    axes.text((y_x_frac - offset) * xmax, y_text_pos, y_label,
            horizontalalignment='right',
            verticalalignment='center',
            fontsize=settings.TINY_FONT_SIZE
            )



def quad_timecourses(figure):
    expt = data.load_data(
            'experimental_data/jegou_2011/sample_filament_timecourse.dat')

    top_left_axes = _quad_sub(figure, 'A', location='tl')
    # Random filaments
    plot_traces(top_left_axes,
            'results/depoly_tc_random.dat',
            color='#80CC80',
            thickness=THIN_LINE)
    # Vectorial filaments
    plot_traces(top_left_axes,
            'results/depoly_tc_vectorial.dat',
            color='#BBBB80',
#            color='#8080FF',
            thickness=THIN_LINE)
    # Vec non be
#    plot_traces(top_left_axes,
#            'results/depoly_nonbe_tc.dat',
#            color='#80FF80', thickness=THIN_LINE)
    # Data on top
    top_left_axes.plot(expt[0], expt[1], 'k.',
            markersize=1, clip_on=False)

    add_scale_bar(top_left_axes, (200, 2))


    # Fast Barbed release
    top_right_axes = _quad_sub(figure, 'B', location='tr')
    plot_traces(top_right_axes,
            'results/depoly_tc_barbed.dat',
            color='#8080FF', thickness=THIN_LINE)
    plot_traces(top_right_axes,
            'results/depoly_mean_barbed.dat',
            color='r', thickness=THICK_LINE)
    # Data on top
    top_right_axes.plot(expt[0], expt[1], 'k.',
            markersize=1, clip_on=False)

    # Cooperative fit
    bottom_left_axes = _quad_sub(figure, 'C', location='bl')
    plot_traces(bottom_left_axes,
            'results/depoly_tc_cooperative.dat',
            color='#8080FF', thickness=THIN_LINE)
    plot_traces(bottom_left_axes,
            'results/depoly_mean_cooperative.dat',
            color='r', thickness=THICK_LINE)
    # Data on top
    bottom_left_axes.plot(expt[0], expt[1], 'k.',
            markersize=1, clip_on=False)

    # jegou's fast rate
    bottom_right_axes = _quad_sub(figure, 'D', location='br')
    plot_traces(bottom_right_axes,
            'results/depoly_tc_jegou.dat',
            color='#8080FF', thickness=THIN_LINE)
    plot_traces(bottom_right_axes,
            'results/depoly_mean_jegou.dat',
            color='r', thickness=THICK_LINE)
    # Data on top
    bottom_right_axes.plot(expt[0], expt[1], 'k.',
            markersize=1, clip_on=False)


def plot_traces(axes, filename, color=None, thickness=1):
    tdat = data.load_data(filename)
    times, values = tdat[0], tdat[1:]
    for y in values:
        y = numpy.array(y)
        y *= 0.0027
        axes.plot(times, y, '-', color=color,
                linewidth=thickness)

def coop_qof(figure):
    coop_data = data.load_data('results/depoly_cooperative_qof.dat')
    vec_data = data.load_data('results/depoly_vectorial_qof.dat')

    rhos, chis, minchis, maxchis, pct_chis = coop_data
    errs = numpy.array(chis) - numpy.array(minchis)

    vchi, vminchi, vmaxchi, vpct_chi = zip(*vec_data)[0]

    with contexts.subplot(figure, (2, 1, 2), title='E',
            x_label=r'$\rho_d$',
            y_label=r'Quality of Fit, $\Delta^2$',
            logscale_x=True) as axes:
        axes.fill_between([0.1, 1.0e12], [vminchi, vminchi],
                vmaxchi, color='#CCCCFF')
        axes.axhline(vchi, 0, 1, color='b', linestyle=':')

        axes.plot(rhos, chis, 'k.')
        axes.errorbar(rhos, chis, errs, fmt='k.')
        axes.set_ylim([0, 8])
        axes.set_xlim([0.1, 10**12])
        axes.set_xticks([1, 100, 10000, 1000000,
            100000000, 10000000000])



# def main(filename='plots/depoly_timecourses.pdf'):
#     with contexts.complex_figure(filename,
# #            height=settings.DOUBLE_COLUMN_DEFAULT_HEIGHT_CM,
# #            width=settings.DOUBLE_COLUMN_DEFAULT_WIDTH_CM) as figure:
#             width=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2,
#             height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM * 2) as figure:
#         random_vectorial_timecourse(figure)
#     #    tip_filaments(figure)
#         tip_fit(figure)
#         rate_fit(figure)
#         cooperative_timecourse(figure)

def tip_fit(figure):
    best_tc = data.load_data('results/depoly_timecourse.dat')

    times, values = numpy.array(best_tc[0]), numpy.array(best_tc[1])
    times -= 300
    values *= 0.0027

    expt = data.load_data(
            'experimental_data/jegou_2011/sample_filament_timecourse.dat')
    etimes, evals = numpy.array(expt[0]), expt[1]

#    with contexts.basic_figure('plots/depoly_tip_fit_timecourse.pdf',
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

#    with contexts.basic_figure('plots/depoly_tip_filaments.pdf',
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

#    with contexts.basic_figure('plots/depoly_tip_filaments.pdf',
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

#    with contexts.basic_figure('plots/depoly_rv_timecourses.pdf',
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

#    with contexts.basic_figure('plots/depoly_coop_timecourses.pdf',
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
