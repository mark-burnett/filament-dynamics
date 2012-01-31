#    Copyright (C) 2011-2012 Mark Burnett
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

import operator
import bisect
import datetime
import itertools
import random
import time

import numpy
import scipy
import scipy.stats

from actin_dynamics import database
from actin_dynamics.numerical import interpolation, utils

from . import logger
log = logger.getLogger(__file__)


# parameters to vary
# search method
#   brent's
#   successive parabolic?
#   our own brew?
# Optimization targets/fitnesses
# End conditions
#   fitness variation across bracket
#   parameter difference (bracket midpoint + fitting error (bracket width / 2)
# track running jobs
#   use polling
# maintain job queue

# what fitting algorithm am I going to use?
#   can I insert fitpy into this whole shebang?
#       the real question is job management, etc.

# what am I actually going to use this for right now?
#   at least fitting melki rates given ftc
#   at most fitting rates + ftcs at once
#   so:
#       at least: 1 parameter, 1 objective
#       at most: 2 parameters, 2 objectives
# therefore, I can scrape by with a simple 1-d search
#   this is the best way to get started
# however, it doesn't make sense to use these simple 1-d searches with
#   parallel function evaluations
#
# ultimately,
#   -> I virtually *have* to use some sort of swarming or genetic algorithm
#   -> I don't have to implement a multi-objective evaluator

# having waiting worker proc's does the following:
#   means that the algorithm has to work with sparse/random data
#       e.g. can't wait for a GA generation to finish
#           -> continuous GA

# I want to be able to resume a session (load existing, then add on new jobs)


# Open questions
#   How big a problem is our statistical/simulation error?
#       Just calculate worst case intervals at each step based on our errors?
#           Log warning when interval grows.
#               (but *do* allow interval to grow..we might have been wrong)
#       calculate optimistic and pessimistic fitness based on reported error?
#           when we kill population, remove the ones with the least upside
#               (lowest "optimistic" fitness)
#           report best fit and best pessimistic fit
#           report overlapping range
#               min/max parameter which overlaps with the best optimistic fit
#               this is our best guess at fitting error
#               * actually this would be a good guess of the fitting error
#                   if we have sampled well near the best fit


class SimplePopulation(object):
    def __init__(self, parameter_guess=None, gaussian_width_fraction=0.06/2,
            parameter_name=None, objective_name=None, dbs=None,
            session=None, process=None, plot=False, max_population_size=None,
            parameter_tolerance=0.00001, parameter_distance_fraction=0.1):
        self.dbs = dbs
        self.session = session

        self.model = session.models[0]
        self.experiment = session.experiments[0]

        self.process = process

        self.objective_name = objective_name
        self.parameter_name = parameter_name

        self.parabola_peak = parameter_guess
        self.gaussian_width_fraction = gaussian_width_fraction

        self.max_population_size = max_population_size

        self.parameter_tolerance = parameter_tolerance
        self.parameter_distance_fraction = parameter_distance_fraction

        self.plot = plot

        self.coeffs = None
        self.last_parabola_peak = self.parabola_peak * 10

        self.pairs = []
        self.inverted_parabola = False
        self._num_completed_jobs = 0


    def log_report(self):
        log.critical('Best fit: %s = %s.',
                self.parameter_name, self.parabola_peak)
        log.critical('Completed %s jobs.', self._num_completed_jobs)



    def add_completed_job(self, job):
        return self.add_completed_jobs([job])

    # It's slightly better to work on a whole list, then update our stats.
    def add_completed_jobs(self, jobs):
        for job in jobs:
            run = job.run
            fitness = run.get_objective(self.objective_name)
            parameter = run.parameters[self.parameter_name]
            
            if fitness is not None:
                bisect.insort(self.pairs, (fitness, parameter))
                self.pairs = self.pairs[:self.max_population_size]

            self._num_completed_jobs += 1

        self.fit_parabola()


    def acceptable_fit(self):
        ordered_y, ordered_x = zip(*sorted(self.pairs,
            key=operator.itemgetter(1)))
        parabola_y = scipy.polyval(self.coeffs, ordered_x)

        if self.plot:
            import matplotlib.pyplot
            pyplot = matplotlib.pyplot

            pyplot.ion()
            pyplot.draw()

            a = pyplot.subplot(1, 1, 1)
            a.clear()

#            a.set_xscale('log')
#            a.set_yscale('log')

            pyplot.plot(ordered_x, ordered_y, 'ro')
            pyplot.plot(ordered_x, parabola_y, 'b-')

            pyplot.axvline(self.parabola_peak, 0, 1,
                    linestyle=':', color='g')

            pyplot.draw()

        return ((self.last_parabola_peak is not None) and
                    ((abs(self.parabola_peak - self.last_parabola_peak)
                        / self.parabola_peak) < self.parameter_tolerance))

#        ordered_x = sorted(self._x)
#        ordered_y = numpy.array(sorted(self._y))
#
#        parabola_fit_differences = numpy.array(self._y
#                - scipy.polyval(self.coeffs, self._x))
#        parabola_fit_differences -= numpy.mean(parabola_fit_differences)
#        parabola_fit_differences /= numpy.sqrt(
#                numpy.var(parabola_fit_differences))
#        parabola_fit_differences = sorted(parabola_fit_differences**2)

#        length = len(parabola_fit_differences)
#
#        data = numpy.array(list(utils.running_total(parabola_fit_differences)))
#        data /= length
#
#        order = 3
#        cdf = scipy.stats.chi2.cdf(parabola_fit_differences, order)


#        self.chi2_difference = sum((data - cdf)**2)/length
#
#        if self.plot:
#            log.info('Best parameter = %s, R2/N = %s, expected error = %s',
#                    self.best_parameter, self.R2/len(self.pairs),
#                    self.chi2_difference)
#            import matplotlib.pyplot
#            pyplot = matplotlib.pyplot
#
#            pyplot.ion()
#            pyplot.draw()
#
#            a = pyplot.subplot(2, 1, 1)
#            a.clear()
#            pyplot.plot(self._x, self._y, 'ro')
#            pyplot.plot(ordered_x, scipy.polyval(self.coeffs, ordered_x), 'b-')
#
#            pyplot.axvline(self.best_parameter, 0, 1,
#                    linestyle=':', color='g')
#
#
#            a = pyplot.subplot(2, 1, 2)
#            a.clear()
#            a.set_xscale('log')
#            pyplot.plot(parabola_fit_differences, data, 'r-')
#            pyplot.plot(parabola_fit_differences, cdf, 'b-')
#
#            pyplot.draw()

    def fit_parabola(self):
        if self.pairs:
            # Choose points for parabolic fit
            if (self.coeffs is not None and not self.inverted_parabola):
                minx = (1 - self.parameter_distance_fraction) * self.parabola_peak
                maxx = (1 + self.parameter_distance_fraction) * self.parabola_peak
                pairs = [(y, x) for y, x in self.pairs if minx < x < maxx]
                if len(pairs) < 5:
                    pairs = self.pairs
            else:
                pairs = self.pairs

            self._y, self._x = zip(*pairs)

            self.coeffs, R2, n, svs, rcond = scipy.polyfit(self._x, self._y,
                    2, full=True)
            self.inverted_parabola = self.coeffs[0] < 0

            self.last_parabola_peak = self.parabola_peak
            self.parabola_peak = - self.coeffs[1] / (2 * self.coeffs[0])
#            self.parabola_peak = scipy.polyval(self.coeffs, self.best_parameter)

#            if R2 > 0:
#                self.R2 = float(R2 / self.parabola_peak)
#            else:
#                self.R2 = R2


    def create_jobs(self, number):
        if self.inverted_parabola or self.parabola_peak < 0:
            # Use the best fit parameter as the center of the gaussian
            center = min(self.pairs)[1]
            return self._gaussian_create_jobs(number, center=center)
        else:
            return self._gaussian_create_jobs(number)

    def _gaussian_create_jobs(self, number, center=None):
        if center is None:
            center = self.parabola_peak
        log.debug('Generating new parameters from a Gaussian: center = %s.',
                center)
        parameters = scipy.stats.norm.rvs(loc=center,
                scale=(center * self.gaussian_width_fraction),
                size=number)
        parameters = filter(lambda x: x >= 0, parameters)

        jobs = []
        with self.dbs.transaction:
            for p in parameters:
                run_pars = {self.parameter_name: p}
                run = _create_run(run_pars, self.model, self.experiment)
                job = database.Job(run=run, creator=self.process)
                jobs.append(job)
        log.info('Created %s new jobs.', number)

        result = set([j.id for j in jobs])
        if None in result:
            result.discard(None)
            log.error('Some jobs not added to the job queue.  Added ids: %s',
                    result)
        return result


class SimpleFitController(object):
    def __init__(self, dbs=None, session=None, process=None, population=None,
            min_queue_size=0, max_queue_size=200, initial_population_size=100,
            polling_period=5, min_iterations=5, max_iterations=1):
        self.dbs = dbs
        self.session = session

        self.process = process

        self.population = population

        if initial_population_size:
            assert initial_population_size >= min_queue_size
            self.initial_population_size = initial_population_size
        else:
            self.initial_population_size = max_queue_size

        self.polling_period = polling_period

        self.min_queue_size = min_queue_size
        self.max_queue_size = max_queue_size

        self.min_iterations = min_iterations
        self.max_iterations = max_iterations

    def run(self):
        t_initial = datetime.datetime.now()
        queued_job_ids = self.population.create_jobs(
                self.initial_population_size)

#        for iteration in xrange(self.max_iterations):
#            # Wait until we drop below our queue size threshold
#            current_queue_size = self.min_queue_size + 1
#            while current_queue_size > self.min_queue_size:
#                time.sleep(self.polling_period)
#
#                current_queue_size = self.dbs.query(database.Job
#                        ).filter_by(creator=self.process
#                        ).filter_by(worker=None
#                        ).filter_by(complete=False).count()
#
#                # While waiting, add the completed jobs to the population
#                newly_completed_jobs = _get_finished_jobs(self.dbs,
#                        queued_job_ids)
#                for job in newly_completed_jobs:
#                    queued_job_ids.discard(job.id)
#                self.population.add_completed_jobs(newly_completed_jobs)
#            
#            # If this fit is good enough, then break.
#            if (iteration >= self.min_iterations
#                    and self.population.acceptable_fit()):
#                break
#
#            # Otherwise, make more jobs
#            newly_queued_job_ids = self.population.create_jobs(
#                    self.max_queue_size - current_queue_size)
#            for new_job_id in newly_queued_job_ids:
#                queued_job_ids.add(new_job_id)
#            log.info('Added %s jobs to the queue.', len(newly_queued_job_ids))
#
#        t_final = datetime.datetime.now()
#
#        total_runtime = t_final - t_initial
#        self.population.log_report()
#        log.critical('Completed %s iterations in %s.',
#                iteration + 1, total_runtime)
#
#        return self.population.parabola_peak


def _create_initial_jobs(dbs, model=None, experiment=None,
        initial_population_size=None,
        parameter_name=None, process=None,
        parameter_min=None, parameter_max=None):
    initial_jobs = []
    with dbs.transaction:
        for i in xrange(initial_population_size):
            run_pars = {parameter_name: _random_value(
                parameter_min, parameter_max)}
            run = _create_run(run_pars, model, experiment)
            job = database.Job(run=run, creator=process)
            initial_jobs.append(job)
    log.info('Created %s initial jobs.', initial_population_size)

    result = set([j.id for j in initial_jobs])
    if None in result:
        result.discard(None)
        log.error('Some jobs not added to the job queue.  Added ids: %s',
                result)
    return result



def _random_value(parameter_min, parameter_max):
    width = parameter_max - parameter_min
    return parameter_min + width * random.random()


def _choose_two(sequence, select_function):
    """
    Picks 2 unique items from the sequence.
    """
    p1 = select_function(sequence)
    p2 = p1
    while p1 == p2:
        p2 = select_function(sequence)
    return p1, p2

def _weighted_choice(sequence, width=None):
    """
        Choose a random element from sequence, weighted toward the
    front of the list.
    """
    if not width:
        width = float(len(sequence))/4
    j = len(sequence)
    while j >= len(sequence):
        j = abs(int(random.normalvariate(0, width)))
    return sequence[j]

def _get_finished_jobs(dbs, queued_job_ids):
    with dbs.transaction:
        result = dbs.query(database.Job).filter_by(complete=True
                ).filter(database.Job.id.in_(queued_job_ids)).all()
    return result

def _create_run(parameters, model, experiment):
    run = database.Run(parameters=parameters, model=model,
            experiment=experiment)
    for bind in experiment.objective_list:
        database.Objective(parameters={}, bind=bind, run=run)
    return run
