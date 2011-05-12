#    Copyright (C) 2010-2011 Mark Burnett
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

def running_total(values):
    """
    Generator that calculates a running total of a sequence.
    """
    total = 0
    for v in values:
        total += v
        yield total

def running_stats(iterable):
    iterable = iter(iterable)
    mean = 0
    variance = 0
    for i, value in enumerate(iterable):
        if i:
            ratio = i / float(i + 1)
        else:
            ratio = 1
        variance += ratio * (value - mean)**2
        mean += float(value - mean) / (i + 1)
        yield mean, math.sqrt(variance / (i + 1))
