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

"""
    This module contains various end conditions for the simulations.
"""

import random

__all__ = ['Duration', 'RandomDuration', 'StateLengthBelow']

class Duration(object):
    __slots__ = ['duration']
    def __init__(self, duration):
        if duration <= 0:
            raise ValueError('Illegal duration.')
        self.duration = duration

    def reset(self):
        pass

    def __call__(self, time, state):
        return time > self.duration

class RandomDuration(Duration):
    __slots__ = ['max_duration']
    def __init__(self, max_duration):
        if max_duration <= 0:
            raise ValueError('Illegal max_duration.')
        self.max_duration = max_duration

    def reset(self):
        self.duration = random.uniform(0, self.max_duration)

class StateLengthBelow(object):
    __slots__ = ['minimum_size']
    def __init__(self, minimum_size):
        self.minimum_size = minimum_size

    def reset(self):
        pass

    def __call__(self, time, state):
        return self.minimum_size > len(state)
