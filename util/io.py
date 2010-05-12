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

def make_filename(input_name, output_dir, output_name, supporting_text=None):
    # If a user name was specified, use that.
    if output_name:
        if output_dir:
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            return os.path.join(output_dir, output_name)
        else:
            return output_name

    if not output_dir:
        output_dir = os.path.splitext(input_name)[0]
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    return os.path.join(output_dir, supporting_text)

def data_filename(analysis_name):
    return os.path.join('/home/mark/a/trunk/data/experiments', analysis_name) + '.dat'
