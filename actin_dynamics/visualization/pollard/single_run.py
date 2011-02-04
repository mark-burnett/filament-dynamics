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
from actin_dynamics.analysis import utils

from .. import measurements
from .. import themes

def plot_run(run, final_pyrene_value=3, theme=None, with_data=True):
    # Get color and style settings.
    if not theme:
        theme = themes.Polymerization(duration=40)

    theme.initialize()

    # Stochastic simulation results.
    factin = accessors.get_factin(run)
    measurements.plot_smooth(factin, label='Stochastic F-actin',
                             **theme('F-actin', 'sim_line'))

    pyrene, pyrene_parameters = accessors.get_pyrene(run)
    pyrene_scale_factor = final_pyrene_value / float(pyrene[1][-1])
    scaled_pyrene = utils.scale_measurement(pyrene, pyrene_scale_factor)
    measurements.plot_smooth(scaled_pyrene, label='Stochastic Pyrene',
                             **theme('pyrene', 'sim_line'))

    adppi = accessors.get_multiple_scaled(run, ['pyrene_adppi_count',
                                                'adppi_count'])
    measurements.plot_smooth(adppi, label='Stochastic F-ADP-Pi-actin',
                             **theme('F-ADP-Pi-actin', 'sim_line'))

    # Pollard data
    if with_data:
        pyrene_data, adppi_data = io.pollard.get_data()

        scaled_pyrene_data = utils.scale_measurement(pyrene_data,
                                                     pyrene_scale_factor)
        measurements.plot_smooth(scaled_pyrene_data, label='Pyrene Data',
                                 **theme('pyrene', 'data_line'))
        measurements.plot_scatter(adppi_data, label='F-ADP-Pi Data',
                                  **theme('F-ADP-Pi-actin', 'data_points'))

    theme.finalize()
