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

_COLORS = [['#06246F', '#2A4380', '#123EAB', '#466FD5', '#6C8AD5'],  # blue
           ['#3F046F', '#582781', '#640CAB', '#9240D5', '#A468D5'],  # purple
           ['#00782D', '#238B49', '#00B945', '#37DC74', '#63DC90'],  # green
           ['#A66F00', '#BF9030', '#FFAB00', '#FFC040', '#FFD173']]  # orange


_default_colors = {'adppi_dark':    _COLORS[2][0],
                   'adppi_light':   _COLORS[2][3],
                   'adppi_light1':  _COLORS[2][1],
                   'adppi_light2':  _COLORS[2][2],
                   'adppi_light3':  _COLORS[2][3],
                   'pyrene_dark':   _COLORS[1][0],
                   'pyrene_light':  _COLORS[1][3],
                   'pyrene_light1': _COLORS[1][1],
                   'pyrene_light2': _COLORS[1][2],
                   'pyrene_light3': _COLORS[1][3],
                   'factin_dark':   _COLORS[0][0],
                   'factin_light':  _COLORS[0][3],
                   'pi_dark':       _COLORS[3][0],
                   'pi_light':      _COLORS[3][3],
                   'pi_light1':     _COLORS[3][1],
                   'pi_light2':     _COLORS[3][2],
                   'pi_light3':     _COLORS[3][3]}


_default_line_styles = {'simulation_line': '-',
                        'data_line':       '--'}

_default_line_widths = {'simulation_line': 2,
                        'data_line':       2}

_default_point_styles = {}
#_default_point_styles = {'data_points': 'o'}

_default_point_sizes = {}
#_default_point_sizes = {'data_points': 16}




class Theme(object):
    def __init__(self, color_scheme=_default_colors,
                 line_styles=_default_line_styles,
                 line_widths=_default_line_widths,
                 point_styles=_default_point_styles,
                 point_sizes=_default_point_sizes):
        self._properties = []

        if color_scheme:
            self._properties.append(dict(
                (k, {'color': v}) for k, v in color_scheme.iteritems()))

        if line_styles:
            self._properties.append(dict(
                (k, {'linestyle': v}) for k, v in line_styles.iteritems()))
        if line_widths:
            self._properties.append(dict(
                (k, {'linewidth': v}) for k, v in line_widths.iteritems()))

        if point_styles:
            self._properties.append(dict(
                (k, {'marker': v}) for k, v in point_styles.iteritems()))
        if point_sizes:
            self._properties.append(dict(
                (k, {'markersize': v}) for k, v in point_sizes.iteritems()))

    def __call__(self, *identifiers):
        result = {}
        for i in identifiers:
            for props in self._properties:
                attribute = props.get(i, {})
                result.update(attribute)
        return result
