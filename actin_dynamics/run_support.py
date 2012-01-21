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

from . import factories

from . import database

from . import logger
log = logger.getLogger(__file__)

def run_job(job, db_session):
    run = job.run
    log.info('Staring job %s: simulation of run %s.', job.id, job.run_id)
    simulation = factories.simulations.make_run(run)
    print 'simulation created'
    try:
        results = simulation.run()
    except object as e:
        print 'simulation failed:'
        print e
    print 'simulation finished'

    for analysis in run.experiment.analysis_list:
        log.debug('Analysing job %s: %s.', job.id, analysis.label)
        a = factories.bindings.db_single(analysis, run.all_parameters)
        analysis_result = a.perform(results, factories.analysis.make_result)
        analysis_result.run = run
        db_session.add(analysis_result)

    log.debug('Calculating %s objectives for job %s.',
              len(run.objectives), job.id)
    for objective in run.objectives:
        log.debug('Calculating objective %s for job %s.',
                  objective.bind.label, job.id)
        o = factories.bindings.db_single(objective.bind,
                                         objective.all_parameters)
        o.perform(job.run, objective)
        log.debug('Storing summary of %s for job %s (%s).',
                  objective.bind.label, job.id, objective.value)

    log.info('Finished job %s.', job.id)
