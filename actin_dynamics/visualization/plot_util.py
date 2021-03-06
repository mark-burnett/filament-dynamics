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

from matplotlib.backends.backend_ps import FigureCanvasPS as _FigureCanvas
from matplotlib.figure import Figure as _Figure

def figure(interactive=False):
    if interactive:
        import pylab
        return pylab.figure()
    f = _Figure()
    canvas = _FigureCanvas(f)
    return f
