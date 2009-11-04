from numpy import array, average, linspace, roll
from scipy.stats import linregress

def _dispersion( L, window_size, step_size ):
    shifted = roll( L, -window_size )
    difference = L[:-window_size] - shifted[:-window_size]
    return average( difference**2 )

def _fluctuations( L, time, dt, n_pts ):
    """
    Determines the Diffusion constant for L.

    L should be adjusted so both its velocity is 0, and its sum is 0.
    """
    values = []
    t_win_sizes = linspace( 100 * dt, time[-1]/2, n_pts )
    window_sizes = [ int(t/dt) for t in t_win_sizes ]
    values = [ _dispersion( array(L), ws, 1 ) for ws in window_sizes ]

    return linregress( 2*t_win_sizes, values )

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
    d, d_const, d_r, d_tt, d_err = _fluctuations( subvalues, time, dt, 1000 )

    return d, v, d_err, v_err
