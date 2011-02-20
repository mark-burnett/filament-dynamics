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

from . import database
from . import meshes

class Controller(object):
    def __init__(self, session, parameter_specifications={}):
        self.session = session
        self.parameter_specifications = parameter_specifications

    def create_jobs(self):
        db_session = database.DBSession()
        for experiment in self.session.experiments:
            expt_par_specs = self.parameter_specifications[experiment.name]
            # loop over run pars
            for run_pars in meshes.parameters_from_spec(
                    expt_par_specs['simulation']):
                r = database.Run(parameters=run_pars, experiment=experiment)
                # loop over objective pars
                for oc in experiment.objective_configurations:
                    obj_def = expt_par_specs['objective'][oc.name]
                    for obj_pars in meshes.parameters_from_spec(obj_def):
                        # create objective
                        o = database.Objective(parameters=obj_pars,
                                               configuration=oc,
                                               run=r)
                # queue job
                j = databse.Job(run=r)
                db_session.add(j)
                db_session.commit()
