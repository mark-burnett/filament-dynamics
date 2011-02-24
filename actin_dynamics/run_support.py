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

from . import factories

def run_job(job):
    # XXX Job starts/completions should be logged.
    print 'running job #', job.id
    simulation = factories.simulations.make_run(job.run)
    full_results = simulation.run()

    db_session = database.DBSession()
    for analysis in run.experiment.analyses:
        a = factories.shortcuts.make_analysis(analysis)
        analysis_result_object = a.perform(full_results,
                                           factories.analysis.make_result)
        db_session.add(analysis_result_object)
    db_session.commit()

    for objective in run.experiment.objectives:
        o = factories.shortcuts.make_objective(objective)
        objective_result_object = o.perform(job.run,
                                            factories.objectives.make_result)
        db_session.add(objective_result_object)
    db_session.commit()
