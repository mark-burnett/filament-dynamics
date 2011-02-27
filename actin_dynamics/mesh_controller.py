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

import operator

from . import database
from .numerical import meshes

from . import logger

log = logger.getLogger(__file__)

class Controller(object):
    def __init__(self, session, parameter_specifications={}):
        self.session = session
        self.parameter_specifications = parameter_specifications

    def create_jobs(self):
        log.info('Creating jobs for %s experiments.' %
                 len(self.session.experiments))
        db_session = database.DBSession()
        # XXX Assume we're only running one model.
        model = self.session.models[0]
        for experiment in self.session.experiments:
            expt_par_specs = self.parameter_specifications[experiment.name]

            # Provide a little extra info for the log.
            num_jobs = reduce(operator.mul,
                    [par['num_points']
                     for par in expt_par_specs.get('simulation',
                                                   {}).itervalues()], 1)
            num_objective_sets = sum((reduce(operator.mul,
                (par['num_points'] for par in obj_set.itervalues()), 1)
                for obj_set in expt_par_specs.get('objective',
                                                  {}).itervalues()))

            log.info("Creating %s jobs for experiment: '%s'." %
                     (num_jobs, experiment.name))
            log.info("Each '%s' job has %s objective calculations." %
                     (experiment.name, num_objective_sets))

            # loop over run pars
            for run_pars in meshes.parameters_from_spec(
                    expt_par_specs['simulation']):
                r = database.Run(parameters=run_pars,
                                 model=model,
                                 experiment=experiment)
                # loop over objective pars
                for obj_name, obj_bind in experiment.objectives.iteritems():
                    obj_def = expt_par_specs.get('objective', {}).get(obj_name,
                                                                      {})
                    for obj_pars in meshes.parameters_from_spec(obj_def):
                        # create objective
                        o = database.Objective(parameters=obj_pars,
                                               bind=obj_bind,
                                               run=r)
                # queue job
                j = database.Job(run=r)
                db_session.add(j)
                db_session.commit()
