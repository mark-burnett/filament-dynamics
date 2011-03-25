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
import bisect

from . import workalike

from actin_dynamics import logger
log = logger.getLogger(__file__)

def make_histogram(values, bin_size):
    bin_size = float(bin_size)
    smallest_relative_index = - get_bin_distance(min(values), bin_size)
    largest_relative_index  =   get_bin_distance(max(values), bin_size)
    log.debug('Smallest value = %s, largest value = %s',
              min(values), max(values))
    log.debug('Smallest index = %s, largest index = %s',
              smallest_relative_index, largest_relative_index)

    edges, centers = make_bins(smallest_relative_index,
                               largest_relative_index, bin_size)
    log.debug('centers %s', centers)
    counts = [0 for b in centers]

    for v in values:
        left_index  = bisect.bisect_left(edges, v)
        right_index = bisect.bisect_right(edges, v, left_index - 1, left_index + 2)
        if left_index != right_index:
            log.error('Bisect indices not equal: left_index = %s, right_index = %s',
                      left_index, right_index)
        counts[left_index - 1] += 1
    log.debug('counts %s', counts)

    pct_error = 1 / math.sqrt(len(values))
    errors = [pct_error * c for c in counts]

    return centers, counts, errors


def get_bin_distance(value, bin_size):
    remaining_distance = abs(value) - bin_size/2
    if remaining_distance > 0:
        return int(math.ceil(float(remaining_distance) / bin_size))
    else:
        return 0

# Add 1 additional bin outside the specified range on each side
def make_bins(smallest_distance, largest_distance, bin_size):
    centers = [bin_size * i for i in xrange(smallest_distance,
                                            largest_distance + 2)]
    edges = [c - bin_size / 2 for c in centers]

#    total_bins = smallest_distance + largest_distance + 3
#    left_boundary  = - (smallest_distance + 1.5) * bin_size
#    right_boundary =   (largest_distance + 1.5)  * bin_size
#
#    left_edges = workalike.linspace(left_boundary, right_boundary, bin_size)
#    centers = [le + bin_size / 2 for le in left_edges]

    return edges, centers
