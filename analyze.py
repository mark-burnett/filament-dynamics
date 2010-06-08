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

import itertools

import baker

import numpy

import analysis.io
import analysis.sampling
import analysis.statistics

@baker.command
def statistics(input_filename, stage_name, property_name, sample_period,
               output_dir=None, output_filename=None):
    """
    Calculate average and standard deviation of 'property_name' measurement
    at time steps specified by 'sample_period'.
    """
    with open(input_filename) as f:
        sim_data, sim_parameters = analysis.io.get_stage_data(f, stage_name)

    # Setup calculations
    property_data = [d[property_name] for d in sim_data]
    sample_times = numpy.arange(0, sim_parameters['duration'],
                                float(sample_period))

    sampled_property_data = analysis.sampling.downsample_each(sample_times,
                                                              property_data)

    averages, std_devs = analysis.statistics.avg_std(sample_times,
                                                     sampled_property_data)

    default_filename = 'statistics_%s.csv' % property_name
    output_filename = analysis.io.create_output_filename(input_filename,
            stage_name, default_filename, output_dir, output_filename)
    
    analysis.io.make_leading_directories(output_filename)

    with open(output_filename, 'w') as of:
        analysis.io.write_csv(of, itertools.izip(sample_times, averages,
                                                 std_devs))

@baker.command
def filament_concentration(input_filename, stage_name, sample_period,
                           luminance_parameter_filename,
                           output_dir=None, output_name=None):
    pass

@baker.command
def mitchison_stability(input_filename, stage_name, sample_period,
                        output_dir=None, output_name=None):
    pass

@baker.command
def phosphate_cleavage(input_filename, stage_name, sample_period,
                       output_dir=None, output_name=None):
    pass

@baker.command
def phosphate_release(input_filename, stage_name, sample_period,
                      output_dir=None, output_name=None):
    pass

@baker.command
def tip_diffusion(input_filename, stage_name, sample_period,
                  output_dir=None, output_name=None):
    pass

baker.run()
