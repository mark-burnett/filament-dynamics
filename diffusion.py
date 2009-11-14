#    Copyright (C) 2009 Mark Burnett
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

from numpy import array, average, roll, var
from scipy.stats import linregress

# Velocity calculations
def fit_velocity(values, dt):
    """
    A least-squares fit to the growth rate.
    """
    time = dt * array( range(len(values)) )
    v, v_const, v_r, v_tt, v_err = linregress( time, values )
    return v

def window_velocity(values, window_size, dt):
    """
    The velocity used inside the naive diffusion calculation.
    """
    shifted    = roll(values, window_size)
    difference = values[window_size:] - shifted[window_size:]
    return average(difference) / (window_size * dt)

# Diffusion calculations
def naive_diffusion(values, window_size, dt):
    """
    The simplest way to do the diffusion calculation.  Check the variance.
    """
    shifted    = roll(values, window_size)
    difference = values[window_size:] - shifted[window_size:]
    return var(difference) / (2 * window_size * dt)

def given_v_diffusion(values, v, window_size, dt):
    """
    Find the diffusion using a given velocity.
    (Find the variance, given the mean.)
    """
    shifted    = roll(values, window_size)
    difference = values[window_size:] - shifted[window_size:]
    return (average(difference**2) - (v * window_size * dt)**2)\
         / (2 * window_size * dt)

def subtracted_v_diffusion(values, v, window_size, dt):
    """
    Find the diffusion using a given velocity by subtracting the v*t line.
    This should be the same result as given_v_diffusion().
    """
    time = dt * array( range(len(values)) )
    subtracted = values - v * time
    shifted    = roll(subtracted, window_size)
    difference = subtracted[window_size:] - shifted[window_size:]
    return average(difference**2) / (2 * window_size * dt)
