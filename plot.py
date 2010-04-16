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

import os
import operator
import itertools

import csv
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
def plot(input_file, save=False, show=False, dump=True, output_dir=None,
         **kwargs):
    """
    Generate plots for data in pickled input_file. (default)

    Additional key word arguments will be passed on to analysis tools.

    :param save:        Whether to save figures.
    :param show:        Whether to display figures on screen.
    :param dump:        Whether to dump csv files of plots.
    """
    # Read file
    with file(input_file) as f:
        pickle = cPickle.load(f)

    # Grab configs
    model_config      = pickle['model_config']
    simulation_config = pickle['simulation_config']

    # Determine which analyses to perform.
    analyses = analysis.provided[simulation_config['simulation_name']]

    # Perform those analyses.
    data    = pickle['data']
    results = []
    for i, stage_analyses in enumerate(analyses):
        stage_results = []
        for a in stage_analyses:
            try:
                data[0].keys()
                stage_results.append(a.perform(data, **kwargs))
            except AttributeError:
                stage_results.append(a.perform(map(operator.itemgetter(i), data)))
        results.append(stage_results)

    # Determine output directory
    if not output_dir:
        output_dir = os.path.splitext(input_file)[0]

    # Create output directory
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Stage names are used to refine directories
    stage_names = simulation_config['stage_sequence']

    # Write results to csv files.
    if dump:
        for stage_name, stage_results, stage_analyses in itertools.izip(
                stage_names, results, analyses):
            # Use a separate directory for each stage?
            if len(stage_names) > 1:
                stage_dir = os.path.join(output_dir, stage_name)
                if not os.path.exists(stage_dir):
                    os.mkdir(stage_dir)
            else:
                stage_dir = output_dir
            # Convert results, and perform write.
            for r, a in itertools.izip(stage_results, stage_analyses):
                with file(os.path.join(stage_dir,
                                       a.filename + '.csv'), 'w') as f:
                    w = csv.writer(f, delimiter=' ')
                    w.writerows(a.csv(r, **kwargs))

    # Generate figures.
    if show or save:
        import pylab # Don't waste time importing for plain CSV dump

        for stage_name, stage_results, stage_analyses in itertools.izip(
                stage_names, results, analyses):
            for r, a in itertools.izip(stage_results, stage_analyses):
                pylab.figure()
                a.plot(r, **kwargs)
                # Save figure.
                if save:
                    if len(stage_names) > 1:
                        stage_dir = os.path.join(output_dir, stage_name)
                        if not os.path.exists(stage_dir):
                            os.mkdir(stage_dir)
                    else:
                        stage_dir = output_dir
                    pylab.savefig(os.path.join(stage_dir, a.filename + '.png'),
                                  **kwargs)

    # Display figures.
    if show:
        pylab.show()

baker.run()
