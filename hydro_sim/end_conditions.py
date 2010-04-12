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
import random

__all__ = ['Counter', 'Timer', 'MaxVariable', 'RandomMaxVariable']

class MaxVariable(object):
    """
    End condition to end when value of 'var_name' exceeds 'var_max'.
    """
    def __init__(self, var_name, var_max):
        self.var_max  = var_max
        self.var_name = var_name

    def reset(self):
        pass

    def __call__(self, **kwargs):
        return self.var_max < kwargs[self.var_name]

class RandomMaxVariable(object):
    """
        End condition to end when value of 'var_name' exceeds a random
    value between 0 and 'var_max'.
    """
    def __init__(self, var_name, var_max):
        self.var_max     = var_max
        self.var_name    = var_name
        self.var_current = random.uniform(0, self.var_max)

    def reset(self):
        self.var_current = random.uniform(0, self.var_max)

    def __call__(self, **kwargs):
        return self.var_current < kwargs[self.var_name]

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
