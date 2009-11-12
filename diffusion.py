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

from numpy import array, average, linspace, roll
from scipy.stats import linregress
import cPickle

def _dispersion( L, window_size, dt ):
    shifted = roll( L, window_size )
    difference = L[window_size:] - shifted[window_size:]
#    cPickle.dump( (window_size, difference), file('herro.p','wb'))
#    assert( False ) # Kill program so we can look at good stuff
#    raise difference
    # NOTE: perhaps this would be more accurate as
    #  avg( diff**2 ) - avg( diff )**2
    # but it only seems to be a 1/100 of a percent difference
#    return average( difference**2 )
    return ( average( difference**2 ) - average( difference )**2 )/(
            2 * window_size * dt )

def _fluctuations( L, time, dt, n_pts ):
    """
    Determines the Diffusion constant for L.

    L should be adjusted so both its velocity is 0, and its sum is 0.
    """
    values = []
#    t_win_sizes = linspace( 100 * dt, time[-1]/2, n_pts )
#    window_sizes = [ int(t/dt) for t in t_win_sizes ]
    window_sizes = array( linspace(10/dt, len(time)/2, n_pts), int )
    values = [ _dispersion( array(L), ws, dt ) for ws in window_sizes ]
#    slope = average(values / (2*t_win_sizes))

    t_win_sizes = dt * array(window_sizes)
    f = file('dco.dat','w')
    for t, v in zip(t_win_sizes, values):
        f.write('%s %s\n' % (t,v))
    f.close()
#    return values[-1], 0, 0, 0, 0
    return average(values), 0, 0, 0, 0

#    return linregress( 2*t_win_sizes, values )

def D_and_V( values, dt ):
    """
    Gives the velocity and diffusion coefficients for values.
    """
    time = dt * array( range(len(values)) )
    # First we get the linear portion of the function (very simple)
    v, v_const, v_r, v_tt, v_err = linregress( time, values )

    # Next we subtract the linear portion for the diffusion calculation
    subvalues = array( values ) - (time * v + v_const)
    # Now the actual diffusion calculation
    d, d_const, d_r, d_tt, d_err = _fluctuations( subvalues, time, dt, 500 )

    return d, v, d_err, v_err
