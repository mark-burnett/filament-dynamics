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

from actin_dynamics import io
from actin_dynamics.analysis import accessors

from .. import measurements
from .. import themes

def kinsim_comparison(run=None, pollard_simulations=False, theme=None):
    # Get color and style settings.
    if not theme:
        theme = themes.Polymerization()

    theme.initialize()

    # My KINSIM Results
    kin_factin_sim, kin_pi_sim, kin_atp_sim = io.pollard.get_kinsim()

    measurements.plot_smooth(kin_factin_sim, label='KINSIM F-actin',
                             **theme('F-actin', 'data_line'))
    measurements.plot_smooth(kin_pi_sim, label='KINSIM Pi',
                             **theme('Pi', 'data_line'))
    measurements.plot_smooth(kin_atp_sim, label='KINSIM F-ATP',
                             **theme('F-ATP-actin', 'data_line'))

    # Pollard simulations
    if pollard_simulations:
        p_factin_sim, p_pi_sim, p_atp_sim = io.pollard.get_simulations()

        measurements.plot_smooth(p_factin_sim, label='Pollard F-actin',
                                 **theme('F-actin', 'sim_line'))
        measurements.plot_smooth(p_pi_sim, label='Pollard Pi',
                                 **theme('Pi', 'sim_line'))
        measurements.plot_smooth(p_atp_sim, label='Pollard F-ATP',
                                 **theme('F-ATP-actin', 'sim_line'))

    # My stochastic simulation
    if run:
        my_factin_sim, my_pi_sim, my_atp_sim = get_kinsim_results(run)

        measurements.plot_smooth(my_factin_sim, label='Stochastic F-actin',
                                 **theme('F-actin', 'sim_line'))
        measurements.plot_smooth(my_pi_sim, label='Stochastic Pi',
                                 **theme('Pi', 'sim_line'))
        measurements.plot_smooth(my_atp_sim, label='Stochastic F-ATP',
                                 **theme('F-ATP-actin', 'sim_line'))

    theme.finalize()

def get_kinsim_results(run):
    factin = accessors.get_factin(run)
    pi     = accessors.get_scaled(run, 'Pi')
    atp    = accessors.get_scaled(run, 'atp_count')
    return factin, pi, atp
