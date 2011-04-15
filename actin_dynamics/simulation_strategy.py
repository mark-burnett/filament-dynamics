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
    This module contains a general Kinetic Monte Carlo simulation.
"""

import math
import random
import collections

from .numerical import utils

from .numerical import rate_bisect

from . import logger

log = logger.getLogger(__file__)

class Simulation(object):
    """
    Kinetic Monte Carlo simulation object.
    """
    __slots__ = ['transitions', 'concentrations', 'measurements',
                 'end_conditions', 'filaments', 'rng']
    def __init__(self, transitions=None, concentrations=None, measurements=None,
                 end_conditions=None, filaments=None, rng=None):
        """
        'transitions' is a list of transition objects.  Each object represents
            a set of possible state changes.
        'measurements' is a list of measurements to perform at each step.
        'end_conditions' is an iterable of end conditions
            (see 'end_conditions' module).
        'filaments' is the list of filaments being simulated.
        'rng' is the random number generator used for the process.
        """
        self.transitions    = transitions
        self.concentrations = concentrations
        self.measurements   = measurements
        self.end_conditions = end_conditions
        self.filaments      = filaments
        self.rng            = rng


    def measure_concentrations(self, time, results):
        conc_results = results['concentrations']
        for name, c in self.concentrations.iteritems():
            conc_results[name].append((time, c.value))

    def run(self, sample_period):
        '''
        Perform the actual simulation, starting with initial_state.
        '''
        # NOTE Aliases for a small speedup in cpython.
        ml  = math.log
        if self.rng is not None:
            rng = self.rng
        else:
            rng = random.uniform

        time = 0
        next_measurement = 0

        results = {'concentrations': collections.defaultdict(list),
                   'filaments': collections.defaultdict(
                       lambda: collections.defaultdict(list))}

        try:
            while not any(e(time, self.filaments, self.concentrations)
                          for e in self.end_conditions):
                transition_Rs = [t.R(self.filaments, self.concentrations)
                                 for t in self.transitions]

                running_transition_R = list(utils.running_total(transition_Rs))
                total_R = running_transition_R[-1]

                # Update simulation time
                if total_R <= 0:
                    log.warn('ENDING SIMULATION:  no possible events.')
                    break;

                # Adjust time first, then record measurements
                # This provides "previous-value interpolation"
                dt = ml(1/rng(0, 1)) / total_R

                if time + dt > next_measurement:
                    self.measure_concentrations(next_measurement, results)
                    for measurement in self.measurements:
                        measurement.perform(next_measurement, self.filaments,
                                            results)
                    next_measurement += sample_period
                time = time + dt

                # Figure out which transition to perform
                transition_r = rng(0, total_R)
                transition_index, remaining_r = rate_bisect.rate_bisect(
                        transition_r, running_transition_R)

                # Finally perform the transition
                self.transitions[transition_index].perform(time, self.filaments,
                        self.concentrations, remaining_r)

        except:
            log.critical(
        'Simulation failed: time = %s, concentrations = %s',
                      time, dict((key, c.value)
                          for key, c in self.concentrations.iteritems()))
            raise


        return results
