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

import math

class ColorScheme(object):
    def __init__(self, colors):
        self.colors = colors

        self.used_colors  = set()
        self.used_analogs = set()

        self.used_lists   = dict((i, 0) for i in xrange(len(colors)))


    def analog(self, count):
        for i, clist in enumerate(self.colors):
            if i not in self.used_analogs:
                if len(clist) < count:
                    self.used_analogs.add(i)
                    colors = select_analogs(clist, count)
                    for c in colors:
                        self.used_colors.add(colors)
                    self.used_lists[i] += len(colors)
                    return colors
        raise RuntimeError('Not enough colors to choose analogs.')


    @property
    def color(self):
        clist = self._get_underused_clist()
        return self._middle_out_search(clist)

    def _get_underused_clist(self):
        best = -1
        best_num = 10**10
        for i, num in self.used_lists.iteritems():
            if num < best_num:
                best = i
                best_num = num
        return self.colors[i]

    def _middle_out_search(self, clist):
        center = math.ceil(float(len(clist) / 2))

        for i in xrange(len(clist)):
            if i % 2:
                index = center - i
            else:
                index = center + i
            color = clist[index]
            if color not in self.used_colors:
                self.used_colors.add(color)
                return color

        raise RuntimeError('Out of colors.')


    def reset(self):
        self.used_colors.clear()
        self.used_analogs.clear()

# XXX This needs a better heuristic.
def select_analogs(clist, count):
    spacing = len(clist) / count
    return clist[:count:spacing]


# Color Scheme Designer 3
# http://colorschemedesigner.com/#3M62fw0w0w0w0
# Rearragned darkest to lightest.
default_colors = [
        ['#06246F', '#2A4380', '#123EAB', '#466FD5', '#6C8AD5'], # blue
        ['#3F046F', '#582781', '#640CAB', '#9240D5', '#A468D5'], # purple
        ['#00782D', '#238B49', '#00B945', '#37DC74', '#63DC90'], # green
        ['#A66F00', '#BF9030', '#FFAB00', '#FFC040', '#FFD173']] # orange
