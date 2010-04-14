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
    show = kwargs.get('show', False)
    dump = kwargs.get('dump', False)
    print save, show, dump
    print input_files, kwargs

@baker.command(default=True)
def plot(input_file, save=True, show=False, dump=False, output_dir=None,
         **kwargs):
    """
    Generate plots for data in pickled input_file. (default)

    Additional key word arguments will be passed on to analysis tools.

    :param save:        Whether to save figures.
    :param show:        Whether to display figures on screen.
    :param dump:        Whether to dump csv files of plots.
    """
    # Read file
    pickle = cPickle.load(file(input_file))

    # Grab configs
    model_config      = pickle['model_config']
    simulation_config = pickle['simulation_config']

    # Determine which data collectors were used.
    dcs = [simulation_config['stages'][sn]['data_collectors']
           for sn in simulation_config['stage_sequence']]

    # Determine which analyses to perform.
    # FIXME terrible function name
    analyses = analysis.get_allowed(dcs)

    # Perform those analyses.
    data    = pickle['data']
    # FIXME should this be flat?
    results = [analysis.perform(a, d) for a in stage_a
                 for d, stage_a in itertools.izip(data, analyses)]

    if dump:
        # TODO dump results to a csv file
        pass

    # Plot that data.
    if show or save:
        import pylab

        # TODO convert results to plots yo.

        for p in plot_data:
            pylab.figure()
            for d in p['data']:
                p['function'](*d)
            for label in p['labels']:
                label['function'](*label['arguments'])
            if save:
                # TODO determine fig_file_name
                pylab.savefig(fig_file_name)

    if show:
        pylab.show()

baker.run()
