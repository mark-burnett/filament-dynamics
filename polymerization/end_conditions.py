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
