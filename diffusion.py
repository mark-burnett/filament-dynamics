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

from numpy import array, average, linspace, roll, var, std
from scipy.stats import linregress
import cPickle

def _dispersion( L, window_size, dt ):
    shifted = roll( L, window_size )
    difference = L[window_size:] - shifted[window_size:]
    return var(difference) / ( 2 * window_size * dt )

def _fluctuations( L, time, dt, n_pts ):
    """
    Determines the Diffusion constant for L.

    L should be adjusted so both its velocity is 0, and its sum is 0.
    """
    values = []
    window_sizes = array( linspace(10/dt, len(time)/2, n_pts), int )
    values = [ _dispersion( array(L), ws, dt ) for ws in window_sizes ]

    t_win_sizes = dt * array(window_sizes)
    f = file('dco.dat','w')
    for t, v in zip(t_win_sizes, values):
        f.write('%s %s\n' % (t,v))
    f.close()
    return values[-1], 0, 0, 0, 0

def D_and_V( values, dt ):
    """
    Gives the velocity and diffusion coefficients for values.
    """
    time = dt * array( range(len(values)) )
    # First we get the linear portion of the function (very simple)
    v, v_const, v_r, v_tt, v_err = linregress( time, values )

    # Next we subtract the linear portion for the diffusion calculation
#    subvalues = array( values ) - (time * v)# + v_const)
    # Now the actual diffusion calculation
    d, d_const, d_r, d_tt, d_err = _fluctuations( values, time, dt, 500 )

    return d, v, d_err, v_err
