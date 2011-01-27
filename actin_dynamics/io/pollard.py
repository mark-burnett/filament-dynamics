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

from . import data

def get_data(pyrene_filename='data/pollard_2002/pyrene_fluorescence.dat',
             adppi_filename='data/pollard_2002/adppi_concentration.dat'):
    pyrene_data = data.load_data(pyrene_filename)
    adppi_data  = data.load_data(adppi_filename)
    return pyrene_data, adppi_data

def get_simulations(length_filename='data/pollard_2002/length_simulation.dat',
                    cleavage_filename='data/pollard_2002/cleavage_simulation.dat',
                    kinsim_filename='data/pollard_2002/kinsim_results.dat'):
    length_data = data.load_data(length_filename)
    cleavage_data = data.load_data(cleavage_filename)
    kinsim_data = data.load_data(kinsim_filename)
    return length_data, cleavage_data, kinsim_data
