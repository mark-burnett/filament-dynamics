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
from . import parameter_queue
from . import pollard

def rank_the_world(analysis_container, atp_weights):
    data = pollard.get_data()
    results = parameter_queue.MultiObjectiveParameterQueue()
    for parameter_set in analysis_container:
        for weight in atp_weights:
            cost = fitness.vector(parameter_set, data=data,
                                  atp_weight=atp_weight)
            results.add((parameter_set, weight), cost)
    return results
