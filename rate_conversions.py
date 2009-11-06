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

def scale_rates( rates, dt ):
    """
    Scales the given rates by dt.
    """
    result = {}
    for instate, p in rates.iteritems():
        if p:
            result[instate] = p * dt
        else:
            result[instate] = None
    return result

def scale_multiple_rates( rates, dt ):
    """
    Scales the given rates by dt.

    Designed to work for situations where there are multiple available
        final states for a given intial state.
    """
    result = {}
    for instate, in_rates in rates.iteritems():
        in_rates_converted = []
        if in_rates:
            ptot = 0
            for p, outstate in in_rates:
                ptot += p * dt
                in_rates_converted.append( (ptot, outstate) )
        result[instate] = in_rates_converted
    return result
