#!/usr/bin/env python
#    Copyright (C) 2010 Mark Burnett
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

"""
    This script performs analysis and generates plots.
"""

import cPickle

import baker

import analysis

@baker.command
def compare(*input_files, **kwargs):
    """
    Supply a list of input pickle files for comparison.

    Takes the same arguments as plot.

    :param input_files: List of pickle files to compare.
    :param save:        Whether to save figures.
    :param dump:        Whether to dump csv of plots.
    """
    if 2 > len(input_files):
        raise RuntimeError('Must supply at least 2 input files to compare.')
    save = kwargs.get('save', False)
    dump = kwargs.get('dump', False)
    print save, dump
    print input_files, kwargs

@baker.command(default=True)
def plot(input_file, show=True, save=False, dump=False, output_dir='',
         **kwargs):
    """
    Generate plots for data in pickled input_file.

    Additional key word arguments will be passed on to analysis tools.

    :param save:        Whether to save figures.
    :param dump:        Whether to dump csv of plots.
    """
    # Read file
    data = cPickle.load(file(input_file))

    # Grab configs
    model_config      = data['model_config']
    simulation_config = data['simulation_config']

    # generate plot data (can be multiprocessed if useful)

    # Generate plots
    if show or save:
        import pylab

        for p in plots:
            pylab.figure()
            pylab.plot(*p)
            if save:
                pylab.savefig(fig_file_name)

    if show:
        pylab.show()

baker.run()
