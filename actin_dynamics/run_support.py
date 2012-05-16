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

from sqlalchemy import schema

import actin_dynamics.factories.analysis
import actin_dynamics.factories.bindings
import actin_dynamics.factories.simulations
from . import factories

from . import database

from . import logger
log = logger.getLogger(__file__)

def perform_simulation(run, db_session):
    simulation = factories.simulations.make_run(run)
    results = simulation.run()

    expected_no_samples = int(run.all_parameters['simulation_duration'] /
            run.all_parameters['sample_period'])

    # We're using exception handling to force the unwinding of this transaction
    with db_session.transaction as transaction:
        log.debug('inside transaction')
        for analysis_bind in run.experiment.analysis_list:
            log.debug('Analysing run %s: %s.', run.id, analysis_bind.label)
            analysis = factories.bindings.db_single(analysis_bind,
                    run.all_parameters)
            analysis.run_id = run.id
            analysis_result = analysis.perform(results,
                    factories.analysis.make_result)
            analysis_result.run_id = run.id
            db_session.add(analysis_result)

        log.debug('Calculating %s objectives for run %s.',
                  len(run.objectives), run.id)
        for objective in run.objectives:
            log.debug('Calculating objective %s for run %s.',
                      objective.bind.label, run.id)
            o = factories.bindings.db_single(objective.bind,
                                             objective.all_parameters)
            o.perform(run, objective)
            log.debug('Storing summary of %s for run %s (%s).',
                      objective.bind.label, run.id, objective.value)

    return True


def run_job(job, db_session, tries=3):
    run = job.run
    log.info('Staring job %s: simulation of run %s.', job.id, job.run_id)

    for i in xrange(tries):
        if perform_simulation(run, db_session):
            break
        else:
            log.error('Job failed, exitting.')
        if tries - 1 == i:
            log.error('Job failed %s times for run %s.', tries, job.run_id)
        else:
            log.warn('Job failed, retrying %s more times', tries - i - 1)

    log.info('End job %s.', job.id)
