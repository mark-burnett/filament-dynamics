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

from . import fitness
from . import dominance_heap
from . import pollard

def rank_the_world(analysis_container, atp_weights, data=None):
    if data is None:
        data = pollard.get_data()
    results = dominance_heap.RankedPopulation()
    for parameter_set in analysis_container:
        for weight in atp_weights:
            cost = fitness.vector(parameter_set, data=data,
                                  atp_weight=weight)
            results.push((parameter_set, weight), cost)
    return results

def best_vs_weight(analysis_container, atp_weights):
    data = pollard.get_data()
    results = []
    for weight in atp_weights:
        results.append(rank_the_world(analysis_container,
                                      [weight], data=data).get_best())
    return results
