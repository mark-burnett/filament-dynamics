#    Copyright (C) 2011 Mark Burnett
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

from actin_dynamics.analysis import interpolation

from . import data

def get_data(**kwargs):
    return get_pyrene_data(**kwargs), get_adppi_data(**kwargs)

def get_pyrene_data(pyrene_filename='data/pollard_2002/pyrene_fluorescence.dat',
                    **kwargs):
    return data.load_data(pyrene_filename)

def get_adppi_data(adppi_filename='data/pollard_2002/adppi_concentration.dat',
                   **kwargs):
    return data.load_data(adppi_filename)


def get_interpolated_pyrene_data(sample_times=None, **kwargs):
    pyrene_data = get_pyrene_data(**kwargs)
    return interpolation.resample_measurement(pyrene_data, sample_times)


def get_simulations(length_filename='data/pollard_2002/length_simulation.dat',
                    cleavage_filename='data/pollard_2002/cleavage_simulation.dat'):
    length_data = data.load_data(length_filename)
    cleavage_data = data.load_data(cleavage_filename)
    return length_data, cleavage_data


def get_kinsim(kinsim_filename='data/pollard_2002/kinsim_results.dat'):
    kinsim_data = data.load_data(kinsim_filename)

    time, factin_d, pi_d, atp_d = kinsim_data

    factin = time, factin_d
    pi     = time, pi_d
    atp    = time, atp_d

    return factin, pi, atp
