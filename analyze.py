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

import numpy
import pylab

from analysis.tools import make_timecourse_histogram, histogram_stats

@baker.command
def length_profiles(input_filename):
    results = cPickle.load(file(input_filename))
    config = results['config']
    length_profiles = results['length_profiles']
    histograms = make_timecourse_histogram(length_profiles)
    timecourse_avg, timecourse_std = histogram_stats(histograms)
    time = numpy.linspace(0, config['true_depolymerization_duration'],
                          float(config['true_depolymerization_duration'])/
                          config['true_sample_period'] - 1)
    print len(time), len(timecourse_avg)
    time = time[:len(timecourse_avg)]
    pylab.errorbar(time, timecourse_avg, timecourse_std)
    pylab.show()

@baker.command
def stability(input_filename):
    results = cPickle.load(file(input_filename))
    config = results['config']
    length_profiles = results['length_profiles']
    num_stable_samples = int(100/config['true_sample_period'])

    length_profiles2 = []
    for lp in length_profiles:
        if len(lp) > num_stable_samples:
            length_profiles2.append(lp)
    length_profiles = length_profiles2

# METHOD: only look at points 100s apart to check.
    rate_profiles = [numpy.array(lp) - numpy.roll(lp, num_stable_samples) for lp in length_profiles]

    stable_rate = 100
    stable_profiles = [numpy.abs(rp) < stable_rate for rp in rate_profiles]

    stable_histograms = make_timecourse_histogram(stable_profiles)
    stable_fraction = [float(sum(sh))/len(sh) for sh in stable_histograms]

    time = numpy.linspace(0, config['true_depolymerization_duration'],
                          float(config['true_depolymerization_duration'])/
                          config['true_sample_period'] - 1)
    time = time[:len(stable_histograms)]
    # Simulation
    pylab.plot(numpy.array(time)/60.0, stable_fraction)
    # Mitchison's data
    mdata = -0.94 * numpy.exp(-(time-90)/(6.9 * 60))+0.94
    pylab.plot(numpy.array(time)/60.0, mdata)
    pylab.ylim(0, 1.1)
    pylab.show()

@baker.command
def raw_plot(input_filename):
    results = cPickle.load(file(input_filename))
    config = results['config']
    length_profiles = results['length_profiles']
    length_profiles = [lp + [0 for i in xrange(int(config['true_depolymerization_duration']/config['true_sample_period']) - len(lp) - 1)] for lp in length_profiles]
    time = numpy.linspace(0, config['true_depolymerization_duration'],
                          float(config['true_depolymerization_duration'])/
                          config['true_sample_period'] - 1)
    [pylab.plot(numpy.array(time)/60.0, lp) for lp in length_profiles]
    pylab.show()

baker.run()
