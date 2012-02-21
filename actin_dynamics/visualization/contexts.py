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

from matplotlib.backends.backend_ps import FigureCanvasPS as _FigureCanvas
from matplotlib.figure import Figure as _Figure

import contextlib
import itertools

from plot_scripts import settings


# Change some MPL default settings
import matplotlib

matplotlib.rc('font', size=settings.DEFAULT_FONT_SIZE)

@ contextlib.contextmanager
def complex_figure(filename, dpi=settings.DPI,
        width=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM,
        height=settings.SINGLE_COLUMN_DEFAULT_SIZE_CM,
        draw_frame=False, right_label=False,
        **unused_kwargs):
    scaled_width = width / settings.CM_SCALE
    scaled_height = height / settings.CM_SCALE

    scaled_top_margin = 1 - settings.TOP_MARGIN / height
    scaled_bottom_margin = settings.BOTTOM_MARGIN / height

    scaled_left_margin = settings.LEFT_MARGIN / width
    scaled_right_margin = 1 - settings.RIGHT_MARGIN / width

    if right_label:
        figure = _Figure(dpi=dpi, frameon=draw_frame,
                linewidth=settings.DEFAULT_FRAME_LINE_WIDTH,
                figsize=(scaled_width, scaled_height),
                subplotpars=matplotlib.figure.SubplotParams(
                    bottom=scaled_bottom_margin,
                    left=scaled_left_margin,
                    right=scaled_right_margin))
    else:
        figure = _Figure(dpi=dpi, frameon=draw_frame,
                linewidth=settings.DEFAULT_FRAME_LINE_WIDTH,
                figsize=(scaled_width, scaled_height),
                subplotpars=matplotlib.figure.SubplotParams(
                    bottom=scaled_bottom_margin,
                    left=scaled_left_margin))

    yield figure

    canvas = _FigureCanvas(figure)

    figure.savefig(filename)

@contextlib.contextmanager
def subplot(figure, location, logscale_x=False, logscale_y=False,
        x_label=None, y_label=None,
        title=None, title_position=0.05,
        **unused_kwargs):
    axes = figure.add_subplot(*location)

    if logscale_x:
        axes.set_xscale('log')
    if logscale_y:
        axes.set_yscale('log')

    if title:
        axes.set_title(title, x=title_position)

    if x_label:
        axes.set_xlabel(x_label, size=settings.LABEL_FONT_SIZE)
    if y_label:
        axes.set_ylabel(y_label, size=settings.LABEL_FONT_SIZE)
    
    yield axes

    for label in itertools.chain(axes.get_xticklabels(),
            axes.get_yticklabels()):
        label.set_size(settings.TICK_FONT_SIZE)

@contextlib.contextmanager
def basic_figure(filename, **kwargs):
    with complex_figure(filename, **kwargs) as figure:
        with subplot(figure, (1, 1, 1), **kwargs) as axes:
            yield axes


# XXX Linewidth is not being set.
def plot(axes, plot_type, #linewidth=settings.DEFAULT_PLOT_LINE_WIDTH,
        *args, **kwargs):
    plt_cmd = getattr(axes, plot_type)
    return plt_cmd(*args, **kwargs)

def add_legend(axes,
#        handle_pad=settings.DEFAULT_LEGEND_HANDLEPAD,
        *args, **kwargs):
#    scaled_handle_pad = handle_pad / settings.CM_SCALE
#    l = axes.legend(handletextpad=scaled_handle_pad, **kwargs)
    l = axes.legend(*args, **kwargs)
    l.draw_frame(False)
    for text in l.get_texts():
        text.set_size(settings.LEGEND_FONT_SIZE)
