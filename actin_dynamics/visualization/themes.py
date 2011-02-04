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

# Color Scheme Designer 3
# http://colorschemedesigner.com/#3M62fw0w0w0w0
blue   = ['#123EAB', '#2A4380', '#06246F', '#466FD5', '#6C8AD5']
purple = ['#640CAB', '#582781', '#3F046F', '#9240D5', '#A468D5']
green  = ['#00B945', '#238B49', '#00782D', '#37DC74', '#63DC90']
orange = ['#FFAB00', '#BF9030', '#A66F00', '#FFC040', '#FFD173']

LENGTH_COLORS = blue
CLEAVAGE_COLORS = orange
ADPPI_COLORS = green

class Theme(object):
    def initialize(self):
        pylab.figure()

    def finalize(self):
        pass

    def __call__(self, *identifiers):
        return {}

# Expected KINSIM identifiers:
#   F-actin, Pi, F-ATP-actin,
#   data, sim
class KINSIM(Theme):
    def finalize(self):
        pylab.xlim(0, 40)
        pylab.ylim(0, 7)
        pylab.legend(loc=5)

    def __call__(self, *identifiers):
        return {}
