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

def make_histogram(values, bin_size):
    smallest_relative_index = get_bin_distance(min(values), bin_size)
    largest_relative_index  = get_bin_distance(max(values), bin_size)

    left_boundaries, centers = make_bins(smallest_relative_index,
                                         largest_relative_index, bin_size)
    counts = [0 for b in centers]

    for v in values:
        index = bisect.bisect_left(left_boundaries, v)
        counts[index] += 1

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
    total_bins = smallest_distance + largest_distance + 3
    left_boundary  = - (smallest_distance + 1.5) * bin_size
    right_boundary =   (largest_distance + 1.5)  * bin_size

    left_edges = workalike.linspace(left_boundary, right_boundary, bin_size)
    centers = [le + bin_size / 2 for le in left_edges]

    return left_edges, centers
