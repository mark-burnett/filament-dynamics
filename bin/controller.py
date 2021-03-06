#!/usr/bin/env python

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

import logging

from actin_dynamics.configuration import command_line_parsers
from actin_dynamics.configuration import ini_parsers

from actin_dynamics import job_control, mesh_controller

import actin_dynamics.factories.controllers
from actin_dynamics import factories, database

logger = logging.getLogger()


def main(session_filename):
    db_session = database.DBSession()
    with job_control.process('controller', db_session) as process:
        session, par_spec = factories.controllers.load_complete_session(
            db_session, session_filename)

        c = mesh_controller.Controller(session, par_spec)
        c.create_jobs(db_session, process)


if '__main__' == __name__:
    namespace = command_line_parsers.controller_process()
    ini_parsers.full_config(namespace.config)

    try:
        main(namespace.session)
    except:
        logger.exception('Exception in controller main.')
        raise
