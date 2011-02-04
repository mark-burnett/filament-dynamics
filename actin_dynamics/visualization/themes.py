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

import pylab

from . import colors

class Theme(object):
    def __init__(self, color_scheme=None):
        if color_scheme:
            self.color_scheme = color_scheme
        else:
            self.color_scheme = colors.ColorScheme(colors.default_colors)

    def initialize(self):
        pylab.figure()

    def finalize(self):
        pass

    def __call__(self, *identifiers):
        result = {}
        for i in identifiers:
            result.update(self.properties[i])
        return result

# Expected Polymerization identifiers:
#   F-actin, Pi, F-ATP-actin, F-ADP-Pi-actin, pyrene
#   data, sim
class Polymerization(Theme):
    def __init__(self, specialized_properties={}, duration=40, **kwargs):
        self.duration = duration
        Theme.__init__(self, **kwargs)

        self.properties = self.default_properties()
        self.properties.update(specialized_properties)

    def default_properties(self):
        # Get colors from scheme.
        fg_colors    = self.color_scheme.analog(2)

        atp_colors   = self.color_scheme.analog(2)
        adppi_colors = self.color_scheme.analog(2)
        adp_colors   = self.color_scheme.analog(2)

        pyrene_color = self.color_scheme.color

        pi_color     = self.color_scheme.color

        return {'F-actin':        {'color': fg_colors[0]},
                'F-ATP-actin':    {'color': atp_colors[0]},
                'F-ADP-Pi-actin': {'color': adppi_colors[0]},
                'F-ADP-actin':    {'color': adp_colors[0]},

                'pyrene':         {'color': pyrene_color},

                'G-actin':        {'color': fg_colors[1]},
                'G-ATP-actin':    {'color': atp_colors[1]},
                'G-ADP-Pi-actin': {'color': adppi_colors[1]},
                'G-ADP-actin':    {'color': adp_colors[1]},
                'Pi':             {'color': pi_color},

                'data_line':      {'linestyle': '-',
                                   'linewidth': 2},
                'sim_line':       {'linestyle': '--',
                                   'linewidth': 2},

                'data_points':    {},
                'sim_points':     {}}

    def finalize(self):
        pylab.xlim(0, self.duration)
        pylab.ylim(0, 7)
        pylab.xlabel('Time (s)')
        pylab.ylabel('Concentration (uM)')
        pylab.legend(loc=4)
