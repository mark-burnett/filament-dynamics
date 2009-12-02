#    Copyright (C) 2009 Mark Burnett
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

from itertools import izip

def uncoupled(states, rates):
    """
    Generates an uncoupled hydrolysis rate dictionary for use in the coupled
    simulation.
    """
    d = {}
    for s1, r in izip(states, rates):
        d[(s1, None)] = r
        for s2 in states:
            d[(s1, s2)] = r
    return d
