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
from actin_dynamics.analysis import accessors, utils, fluorescence

from .. import measurements
from .. import themes

def plot_run(run, final_pyrene_value=3, with_data=True,
             pyrene_color=None, adppi_color=None, length_color=None,
             pyrene_normalization_name='pollard_flat_pyrene_normalization',
             pyrene_only=False,
             **kwargs):

    # Stochastic simulation results.
    pyrene = accessors.get_run_pyrene(run, pyrene_normalization_name)
    pyrene_scale_factor = final_pyrene_value / float(pyrene[1][-1])
    scaled_pyrene = utils.scale_measurement(pyrene, pyrene_scale_factor)
    measurements.plot_smooth(scaled_pyrene, label='Stochastic Pyrene',
                             color=pyrene_color, **kwargs)

    if not pyrene_only:
        factin = accessors.get_factin(run)
        measurements.plot_smooth(factin, label='Stochastic F-actin',
                                 color=length_color, **kwargs)

        adppi = accessors.get_multiple_scaled(run, ['pyrene_adppi_count',
                                                    'adppi_count'])
        measurements.plot_smooth(adppi, label='Stochastic F-ADP-Pi-actin',
                                 color=adppi_color, **kwargs)

    # Pollard data
    if with_data:
        pyrene_data = io.pollard.get_interpolated_pyrene_data(pyrene[0])
        adppi_data  = io.pollard.get_adppi_data()
#        pyrene_data, adppi_data = io.pollard.get_data()

        fit, norm = fluorescence._pyrene_normalization(pyrene_data,
                                                       scaled_pyrene)
        scaled_pyrene_data = utils.scale_measurement(pyrene_data, norm)
        measurements.plot_smooth(scaled_pyrene_data, #label='Pyrene Data',
                                 color=pyrene_color, **kwargs)
        if not pyrene_only:
            measurements.plot_scatter(adppi_data, label='F-ADP-Pi Data',
                                      color=adppi_color)
