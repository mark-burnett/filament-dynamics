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

import os
import csv

import cPickle

def get_stage_data(file_, stage_name):
    sim_results = cPickle.load(file_)

    # Grab stage parameters.
    stage_parameters = sim_results['experiment_parameters']['experiment']
    stage_parameters.update(sim_results['experiment_parameters']['stages'][stage_name])

    # Extract stage data.
    stage_index    = sim_results['experiment_config']['stages'].index(stage_name)
    stage_data     = [d[stage_index] for d in sim_results['data']]

    return stage_data, stage_parameters

def create_output_filename(input_filename, stage_name, default_filename,
                           output_dir, output_filename):
    if output_filename:
        if output_dir:
            return os.path.join(output_dir, output_filename)
        else:
            return output_filename

    filename_base, input_ext = os.path.splitext(input_filename)
    filename = os.path.join(filename_base, stage_name, default_filename)

    return filename

def make_leading_directories(output_filename):
    left, right = os.path.split(output_filename)
    if left:
        make_leading_directories(left)
        if not os.path.exists(left):
            os.mkdir(left)

def write_csv(file_, output_iterator):
        w = csv.writer(file_, delimiter=' ')
        w.writerows(output_iterator)

def write_csv_to_filename(output_filename, output_iterator):
    make_leading_directories(output_filename)

    with open(output_filename, 'w') as of:
        write_csv(of, output_iterator)
