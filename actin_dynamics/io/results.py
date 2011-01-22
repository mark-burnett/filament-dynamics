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
import fnmatch

from . import compressed

def get_sim_filenames(directory):
    return [os.path.join(directory, f)
            for f in os.listdir(directory) if fnmatch.fnmatch(f, '*.sim')]

def load_directory(directory):
    files = get_sim_filenames(directory)
    return compressed.combine_files(files)
