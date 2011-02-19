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

class Controller(object):
    def __init__(self, session, parameter_specifications={}):
        self.session = session
        self.parameter_specifications = parameter_specifications

#    def resume_session(self):
#        db_session = database.DBSession()
#        query = db_session.query(database.Session).filter_by(name=self.name)
#
#        # XXX Should be done with logging...
#        if query.count() > 1:
#            print 'WARNING:  More than one matching session found to resume.'
#
#        self.session = query.first()

    def create_jobs(self):
        for experiment in self.session.experiments:
            expt_par_specs = self.parameter_specifications[experiment.name]
            # loop over run pars
                # create run
                # loop over objective pars
                    # create objective
                # queue job
