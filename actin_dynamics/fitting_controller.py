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

import bisect
import datetime
import random
import time

from actin_dynamics import database
from actin_dynamics.numerical import interpolation

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

class Population(object):
    def __init__(self, dbs, process=None, minimize=None,
            model=None, experiment=None, max_size=100,
            parameter_name=None, objective_name=None,
            mutation_rate=0.1, spontaneous_rate=0.05, shooting_rate=0.05,
            mutation_scale=0.05, parameter_min=None, parameter_max=None):
        self.dbs = dbs

        self.model = model
        self.experiment = experiment

        self.parameter_name = parameter_name
        self.objective_name = objective_name

        self.minimize = minimize
        self.max_size = max_size

        self.mutation_rate = mutation_rate
        self.spontaneous_rate = spontaneous_rate
        self.shooting_rate = shooting_rate

        self.mutation_scale = mutation_scale

        self.parameter_min = parameter_min
        self.parameter_max = parameter_max

        self.process = process

        self._fitness_tuples = []
        self._num_completed_jobs = 0
        self._num_started_jobs = 0

    def log_report(self):
        best = self._fitness_tuples[0]
        log.critical('Best fit: %s = %s, fitness = %s, run_id = %s.',
                self.parameter_name, best[1], best[0], best[2].id)
        log.critical('Completed %s jobs.', self._num_completed_jobs)

    def get_best_parameter(self):
        try:
            fitness, parameter, run = self._fitness_tuples[0]
            if not self.minimize:
                fitness = - fitness
            return parameter, fitness
        except IndexError:
            return None, None

    def get_best_run(self):
        fitness, parameter, run = self._fitness_tuples[0]
        return run

    def add_completed_job(self, job):
        run = job.run
        fitness = self._get_fitness(run)
        parameter = run.parameters[self.parameter_name]
        fitness_tuple = fitness, parameter, run

        bisect.insort_left(self._fitness_tuples, fitness_tuple)

        if len(self._fitness_tuples) > self.max_size:
            dead = self._fitness_tuples.pop()
            log.debug(
                'Removed genome from population: %s = %s, fitness = %s.',
                self.parameter_name, dead[1], dead[0])
        self._num_completed_jobs += 1

    def create_jobs(self, number):
        new_jobs = []
        with self.dbs.transaction:
            for i in xrange(number):
                par_value = self._get_child_parameter()
                run_pars = {self.parameter_name: par_value}
                run = _create_run(run_pars, self.model, self.experiment)

                job = database.Job(run=run, creator=self.process)
                new_jobs.append(job)
                log.debug('Creating job for %s = %s.',
                        self.parameter_name, par_value)

        result = set([j.id for j in new_jobs])
        if None in result:
            result.discard(None)
            log.error('Some jobs not added to the job queue.  Added ids: %s',
                    result)
        self._num_started_jobs += len(result)
        return result

    def _get_fitness(self, run):
        for o in run.objectives:
            if self.objective_name == o.bind.label:
                if self.minimize:
                    return o.value
                else:
                    return -o.value
        log.warn('Fitting objective %s not found.', self.objective_name)

    def _get_child_parameter(self):
        r = random.random()
        # Chance for arbitrary mutation.
        if not self._fitness_tuples or r < self.spontaneous_rate:
            new_parameter = _random_value(self.parameter_min,
                    self.parameter_max)
        # Chance to mutate single parent.
        elif r < (self.mutation_rate + self.spontaneous_rate):
            parent_parameter, parent_fitness = self._select_parent()
            delta = parent_parameter * self.mutation_scale
            new_parameter = _random_value(parent_parameter - delta,
                    parent_parameter + delta)
        # Chance to use derivative to find next child
        elif r < (self.mutation_rate + self.spontaneous_rate + self.shooting_rate):
            success = False
            for i in xrange(100):
                a, b = _choose_two(self._fitness_tuples, _weighted_choice)
                a_fit, a_par = a[0], a[1]
                b_fit, b_par = b[0], b[1]
                try:
                    new_parameter = interpolation.simple_zero(a_par, a_fit,
                            b_par, b_fit)
                    success = True
                    break
                except:
                    pass
            if not success:
                new_parameter = _random_value(self.parameter_min,
                        self.parameter_max)
        # Chance to combine parents.
        else:
            a_par, b_par = self._select_two_parameters()
            min_par = min(a_par, b_par)
            max_par = max(a_par, b_par)
            new_parameter = _random_value(min_par, max_par)

        return new_parameter

    def _select_parent(self):
        fitness, parameter, job = _weighted_choice(self._fitness_tuples)
        return parameter, fitness

    def _select_two_parameters(self):
        a, b = _choose_two(self._fitness_tuples, _weighted_choice)
        return a[1], b[1]


class SimpleFitController(object):
    def __init__(self, dbs, session, objective_name, parameter_name,
            parameter_min, parameter_max,
            process,
            min_queue_size=0, max_queue_size=20,
            initial_population_size=40, max_population_size=50,
            polling_period=5, minimize=True,
            min_iterations=2, max_iterations=100,
            parameter_tolerance=0.001, fitness_tolerance=0.1):

        self.dbs = dbs
        self.session = session

        self.objective_name = objective_name
        self.parameter_name = parameter_name

        self.parameter_min = parameter_min
        self.parameter_max = parameter_max

        self.process = process

        if initial_population_size:
            assert initial_population_size >= min_queue_size
            self.initial_population_size = initial_population_size
        else:
            self.initial_population_size = max_queue_size

        self.max_population_size = max_population_size

        self.polling_period = polling_period

        # XXX set lt/gt operator to left/right better ops
        #       or transformation (-f or 1/(1+f))
        self.minimize = minimize

        self.min_queue_size = min_queue_size
        self.max_queue_size = max_queue_size

        self.min_iterations = min_iterations
        self.max_iterations = max_iterations
        self.parameter_tolerance = parameter_tolerance
        self.fitness_tolerance = fitness_tolerance

    def run(self):
        log.debug('Running fit for %s', self.parameter_name)
        # XXX We assume we're only running one model and one experiment.
        model = self.session.models[0]
        experiment = self.session.experiments[0]

        # We need to keep track of:
        #   started/running or finished job ids
        #   queued job ids
        queued_job_ids = _create_initial_jobs(self.dbs,
                model=model, experiment=experiment,
                initial_population_size=self.initial_population_size,
                parameter_name=self.parameter_name, process=self.process,
                parameter_min=self.parameter_min,
                parameter_max=self.parameter_max)

        population = Population(self.dbs, process=self.process,
                minimize=self.minimize,
                model=model, experiment=experiment,
                parameter_name=self.parameter_name,
                objective_name=self.objective_name,
                parameter_min=self.parameter_min,
                parameter_max=self.parameter_max,
                max_size=self.max_population_size)

        t_initial = datetime.datetime.now()
        best_parameter = None
        best_fit = None
        for iteration in xrange(self.max_iterations):
            # Wait until we drop below our queue size threshold
            current_queue_size = self.min_queue_size + 1
            while current_queue_size > self.min_queue_size:
                time.sleep(self.polling_period)

                current_queue_size = self.dbs.query(database.Job
                        ).filter_by(creator=self.process
                        ).filter_by(worker=None
                        ).filter_by(complete=False).count()

                # While waiting, add the completed jobs to the population
                newly_completed_jobs = _get_finished_jobs(self.dbs,
                        queued_job_ids)
                for job in newly_completed_jobs:
                    queued_job_ids.discard(job.id)
                    population.add_completed_job(job)

            previous_parameter = best_parameter
            previous_fit = best_fit
            best_parameter, best_fit = population.get_best_parameter()

            log.info('Iteration %s: best %s = %s, fitness = %s',
                    iteration + 1, self.parameter_name, best_parameter,
                    best_fit)

            if previous_parameter is not None and previous_fit is not None:
#                relative_parameter_change = abs(best_parameter - previous_parameter)
#                relative_fit_change = abs(best_fit - previous_fit)
#                if (relative_parameter_change < best_parameter * self.parameter_tolerance and
                if (best_fit < self.fitness_tolerance and
                    iteration > self.min_iterations):
                    break

            newly_queued_job_ids = population.create_jobs(
                    self.max_queue_size - current_queue_size)
            for new_job_id in newly_queued_job_ids:
                queued_job_ids.add(new_job_id)
            log.info('Added %s jobs to the queue.', len(newly_queued_job_ids))

        t_final = datetime.datetime.now()

        total_runtime = t_final - t_initial
        population.log_report()
        log.critical('Completed %s iterations in %s.',
                iteration + 1, total_runtime)
        return best_parameter, best_fit, population.get_best_run()

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
        width = float(len(sequence))/2
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
