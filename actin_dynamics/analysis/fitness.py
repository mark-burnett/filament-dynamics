#    Copyright (C) 2010 Mark Burnett
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

import itertools

from . import pollard

def vector(parameter_set, data=None,
           functions=(pollard.pyrene_fit,), **kwargs):
#           functions=(pollard.pyrene_fit, pollard.adppi_fit,), **kwargs):
    return [f(parameter_set, d, **kwargs)
            for f, d in itertools.izip(functions, data)]
