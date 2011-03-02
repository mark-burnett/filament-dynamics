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
from . import logger

from . import database

from . import logger
log = logger.getLogger(__file__)

def run_job(job, db_session):
    run = job.run
    num_sims = int(run.all_parameters['number_of_simulations'])
    log.info('Staring job %s: %s simulations of run %s.', job.id,
             num_sims, job.run_id)
    results = []
    for i in xrange(num_sims):
        log.debug('Starting job %s simulation %s.', job.id, i + 1)
        simulation = factories.simulations.make_run(run)
        results.append(simulation.run())

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
        log.debug('Storing summary of objective %s for job %s.',
                  objective.bind.label, job.id)
        store_summary_information(objective)

    log.info('Finished job %s.', job.id)

def store_summary_information(objective):
    parameters = objective.all_parameters
    values = dict((col_name, parameters[par_name])
                  for par_name, col_name in
    # XXX Stupid 0....
                      objective.bind.slice_definition[0].column_map.iteritems())
#    log.debug('Storing value = %s for objective_id = %s',
#              objective.value, objective.id)
    values['objective_id'] = objective.id
    values['value'] = objective.value

    # XXX Stupid 0....
    table = schema.Table(objective.bind.slice_definition[0].table_name,
                         database.global_state.metadata,
                         autoload=True)
    table.insert(values).execute()
