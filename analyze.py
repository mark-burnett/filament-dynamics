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
def raw_plot(input_filename, number=-1):
    results = cPickle.load(file(input_filename))
    config = results['config']
    length_profiles = results['length_profiles']
    length_profiles = [lp + [0 for i in xrange(int(config['true_depolymerization_duration']/config['true_sample_period']) - len(lp) - 1)] for lp in length_profiles]
    time = numpy.linspace(0, config['true_depolymerization_duration'],
                          float(config['true_depolymerization_duration'])/
                          config['true_sample_period'] - 1)
    if len(length_profiles) > 1:
        [pylab.plot(numpy.array(time)/60.0, lp) for lp in length_profiles[:number]]
    else:
        pylab.plot(numpy.array(time)/60.0, length_profiles[0])
    pylab.show()

@baker.command
def stab_var(center_filename, down_filename, up_filename,
             title='Stability Variation'):
    cresults = cPickle.load(file(center_filename))
    dresults = cPickle.load(file(down_filename))
    uresults = cPickle.load(file(up_filename))
    cconfig = cresults['config']
    dconfig = dresults['config']
    uconfig = uresults['config']
    clength_profiles = cresults['length_profiles']
    dlength_profiles = dresults['length_profiles']
    ulength_profiles = uresults['length_profiles']
    num_stable_samples = int(100/cconfig['true_sample_period'])

#    length_profiles2 = []
#    for lp in length_profiles:
#        if len(lp) > num_stable_samples:
#            length_profiles2.append(lp)
#    length_profiles = length_profiles2

# METHOD: only look at points 100s apart to check.
    crate_profiles = [numpy.array(lp) - numpy.roll(lp, num_stable_samples) for lp in clength_profiles]
    drate_profiles = [numpy.array(lp) - numpy.roll(lp, num_stable_samples) for lp in dlength_profiles]
    urate_profiles = [numpy.array(lp) - numpy.roll(lp, num_stable_samples) for lp in ulength_profiles]

    stable_rate = 100
    cstable_profiles = [numpy.abs(rp) < stable_rate for rp in crate_profiles]
    dstable_profiles = [numpy.abs(rp) < stable_rate for rp in drate_profiles]
    ustable_profiles = [numpy.abs(rp) < stable_rate for rp in urate_profiles]

    cstable_histograms = make_timecourse_histogram(cstable_profiles)
    cstable_fraction = [float(sum(sh))/len(sh) for sh in cstable_histograms]

    dstable_histograms = make_timecourse_histogram(dstable_profiles)
    dstable_fraction = [float(sum(sh))/len(sh) for sh in dstable_histograms]

    ustable_histograms = make_timecourse_histogram(ustable_profiles)
    ustable_fraction = [float(sum(sh))/len(sh) for sh in ustable_histograms]

    ctime = numpy.linspace(0, cconfig['true_depolymerization_duration'],
                          float(cconfig['true_depolymerization_duration'])/
                          cconfig['true_sample_period'] - 1)
    ctime = ctime[:len(cstable_histograms)]

    dtime = numpy.linspace(0, dconfig['true_depolymerization_duration'],
                          float(dconfig['true_depolymerization_duration'])/
                          dconfig['true_sample_period'] - 1)
    dtime = dtime[:len(dstable_histograms)]

    utime = numpy.linspace(0, uconfig['true_depolymerization_duration'],
                          float(uconfig['true_depolymerization_duration'])/
                          uconfig['true_sample_period'] - 1)
    utime = utime[:len(ustable_histograms)]

    # Simulation
    pylab.plot(numpy.array(ctime)/60.0, cstable_fraction, 'k')
    pylab.plot(numpy.array(dtime)/60.0, dstable_fraction, 'b')
    pylab.plot(numpy.array(utime)/60.0, ustable_fraction, 'r')
    # Mitchison's data
    mdata = -0.94 * numpy.exp(-(ctime-90)/(6.9 * 60))+0.94
    pylab.plot(numpy.array(ctime)/60.0, mdata, 'g')
    pylab.ylim(0, 1.1)
    pylab.show()

baker.run()
