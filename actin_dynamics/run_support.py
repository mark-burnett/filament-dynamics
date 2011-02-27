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

from . import factories
from . import logger

log = logger.getLogger(__file__)

def run_job(job):
    log.info('Staring job %s.' % job.id)
    run = job.run
    results = []
    for i in xrange(run.parameters['number_of_simulations']):
        log.debug('Starting job %s simulation %s.' % (job.id, i))
        simulation = factories.simulations.make_run(run)
        results.append(simulation.run())

    db_session = database.DBSession()
    for analysis in run.experiment.analyses:
        log.debug('Starting job %s analysis %s.' % (job.id, analysis.name))
        a = factories.bindings.db_single(analysis)
        analysis_result = a.perform(results, factories.analysis.make_result)
        analysis_result.run = run
        db_session.add(analysis_result)
    db_session.commit()

    # XXX there should be objective parameters that show up here.
    for objective in run.experiment.objectives:
        o = factories.bindings.db_single(objective)
        objective_result = o.perform(job.run, factories.objectives.make_result)
        objective_result.bind = objective
        db_session.add(objective_result)
    db_session.commit()

    log.info('Finished job %s.' % job.id)
