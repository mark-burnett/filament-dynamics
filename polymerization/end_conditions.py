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

import datetime

__all__ = ['Counter', 'Timer']

class Counter(object):
    """
    End condition to specify a maximum number of iterations to run.
    """
    def __init__(self, num_iterations):
        self.num_left     = num_iterations
        self.num_starting = num_iterations

    def __call__(self, **kwargs):
        self.num_left -= 1
        return 0 >= self.num_left

    def reset(self):
        self.num_left = self.num_starting

class Timer(object):
    """
    End condition to specify a maximum amount of time to run (approximate).
    """
    def __init__(self, run_duration):
        """
        run_duration is the amount of time to run the simulation.
            Must be a datetime.timedelta() object.
        """
        self.run_duration = run_duration
        self.finish_time  = datetime.datetime.now() + run_duration

    def __call__(self, **kwargs):
        return self.finish_time < datetime.datetime.now()

    def reset(self):
        self.finish_time  = datetime.datetime.now() + self.run_duration
