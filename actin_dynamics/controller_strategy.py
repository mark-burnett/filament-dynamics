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
from . import factories

class Controller(object):
    def __init__(self, name=None, parameter_generators={}, parameters={},
                 model={}, experiments={}):
        self.name = name
        self.parameter_generators = parameter_generators

        self.parameters  = parameters
        self.model       = model
        self.experiments = experiments

    def resume_session(self):
        db_session = database.DBSession()
        query = db_session.query(database.Session).filter_by(name=self.name)

        # XXX Should be done with logging...
        if query.count() > 1:
            print 'WARNING:  More than one matching session found to resume.'

        self.session = query.first()

    def create_static_session(self):
        session = database.Session(name=self.name)
        session.parameters = self.parameters

        session.models.append(factories.database.model(self.model))
        session.experiments = factories.database.static_experiments(
                self.experiments)

        db_session = database.DBSession()
        db_session.add(session)
        db_session.commit()
        self.session = session

    def run(self):
        # setup session, experiments, model

        # loop
            # setup sim + ana
            # add run job
            # setup objective config
            # add objective job(s)
        pass
