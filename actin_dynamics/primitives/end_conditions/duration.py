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

"""
    This module contains various end conditions for the simulations.
"""

from base_classes import EndCondition

import random

class Duration(EndCondition):
    'End simulation after duration seconds.'

    __slots__ = ['duration']
    def __init__(self, duration=None, label=None):
        if duration is None or duration <= 0:
            raise ValueError('Illegal duration.')
        self.duration = duration
        EndCondition.__init__(self, label=label)

    def __call__(self, time, state):
        result = time > self.duration
        return time > self.duration

class RandomDuration(Duration):
    'End simulation after 0 to max_duration seconds.'

    __slots__ = []
    def __init__(self, max_duration=None, min_duration=0, label=None):
        if max_duration is None or max_duration <= 0:
            raise ValueError('Illegal max_duration.')
        if min_duration < 0:
            raise ValueError('Illegal min_duration.')

        Duration.__init__(self, label=label,
                duration=random.uniform(min_duration, max_duration))
