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

    # Determine which analyses to perform.
    analyses = analysis.provided[simulation_config['simulation_name']]

    # Perform those analyses.
    data    = pickle['data']
    results = []
    for i, stage_analyses in enumerate(analyses):
        stage_results = None
        for a in stage_analyses:
            stage_results = [a.perform(d) for d in
                             map(operator.itemgetter(i), data, **kwargs)]
        results.append(stage_results)

    # Determine output directory
    if not output_dir:
        output_dir = os.path.splitext(input_file)

    # Create output directory
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Write results to csv files.
    if dump:
        for stage_results, stage_analyses in itertools.izip(results, analyses):
            for r, a in itertools.izip(stage_results, stage_analyses):
                with file(os.path.join(output_dir, a.filename), 'w') as f:
                    w = csv.writer(f, a.csv(r))

    # Generate figures.
    if show or save:
        import pylab # Don't waste time importing for plain CSV dump

        for stage_results, stage_analyses in itertools.izip(results, analyses):
            for r, a in itertools.izip(stage_results, stage_analyses):
                pylab.figure()
                a.plot(r, **kwargs)
                # Save figure.
                if save:
                    pylab.savefig(os.path.join(output_dir, a.filename),
                                  **kwargs)

    # Display figures.
    if show:
        pylab.show()

baker.run()
