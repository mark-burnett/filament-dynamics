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

import bisect
import cPickle

import baker

import numpy
import pylab

from analysis.tools import make_timecourse_histogram, histogram_stats

def get_stability_values(input_filename, sample_period,
                         stable_time, stable_variation):
    data = cPickle.load(file(input_filename))

    config = data['config']
    time = numpy.linspace(0, config['depolymerization_duration'],
                          float(config['depolymerization_duration'])/
                          sample_period - 1)

    stable_samples = int(stable_time/sample_period)
    # Sample the data
    length_profiles = []
    for r in data['results']:
        # Use interpolation to figure out the values
        lp = numpy.interp(time, r['time'], r['length'], right=-1)
        final_i = -1
        for i, v in enumerate(lp):
            if -1 == v:
                final_i = i
                break
        lp = lp[:final_i]
        if stable_samples < len(lp):
            length_profiles.append(lp)

    # Look at points stable_time seconds apart to check for stability.
    rate_profiles = [numpy.array(lp) - numpy.roll(lp, stable_samples)
                     for lp in length_profiles]

    stable_profiles = [numpy.abs(rp) < stable_variation for rp in rate_profiles]

    stable_histograms = make_timecourse_histogram(stable_profiles)
    stable_fraction = [float(sum(sh))/len(sh) for sh in stable_histograms]

    time = time[:len(stable_fraction)]
    return time, stable_fraction

@baker.command
def stability(input_filename,
              title=None,
              sample_period=20,
              stable_time=100, stable_variation=100):
    time, stable_fraction = get_stability_values(input_filename,
                                sample_period, stable_time, stable_variation)
    # Simulation
    pylab.plot(time/60.0, stable_fraction)
    # Mitchison's data
    mdata = -0.94 * numpy.exp(-(time-90)/(6.9 * 60))+0.94
    pylab.plot(numpy.array(time)/60.0, mdata)
    pylab.ylim(0, 1.1)
    pylab.xlabel('Depolymerization Time (min)')
    pylab.ylabel('Fraction of Stable Filaments')
    pylab.show()

@baker.command
def raw_plot(input_filename, number=-1):
    data = cPickle.load(file(input_filename))
    for r in data['results'][:number]:
        pylab.plot(numpy.array(r['time'])/60, r['length'])

    pylab.xlabel('Depolymerization Time (min)')
    pylab.ylabel('Filament Length (subunits)')
    pylab.show()

@baker.command
def stab_var(center_filename, down_filename, up_filename,
             title=None,
             sample_period=20,
             stable_time=100, stable_variation=100):

    ctime, cstable_fraction = get_stability_values(center_filename,
            sample_period, stable_time, stable_variation)
    dtime, dstable_fraction = get_stability_values(down_filename,
            sample_period, stable_time, stable_variation)
    utime, ustable_fraction = get_stability_values(up_filename,
            sample_period, stable_time, stable_variation)

    # Simulation
    pylab.plot(ctime/60.0, cstable_fraction, 'k')
    pylab.plot(utime/60.0, ustable_fraction, 'b')
    pylab.plot(dtime/60.0, dstable_fraction, 'r')

    # Mitchison's data
    mdata = -0.94 * numpy.exp(-(ctime-90)/(6.9 * 60))+0.94
    pylab.plot(numpy.array(ctime)/60.0, mdata, 'g')
    pylab.ylim(0, 1.1)
    pylab.xlabel('Depolymerization Time (min)')
    pylab.ylabel('Fraction of Stable Filaments')
    pylab.title(title)
    pylab.show()

baker.run()
