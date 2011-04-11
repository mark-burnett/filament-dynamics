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
from actin_dynamics.configuration import logger as logger_config

from actin_dynamics import mesh_controller, process_control
from actin_dynamics import factories, database

logger = logging.getLogger()


def main(session_filename, log_dict):
    db_session = database.DBSession()
    with process_control.process('controller', db_session) as process:
        logger_config.setup_logging_from_dict(log_dict)
        session, par_spec = factories.controllers.load_complete_session(
            db_session, session_filename)

        c = mesh_controller.Controller(session, par_spec)
        c.create_jobs(db_session, process)


if '__main__' == __name__:
    namespace = command_line_parsers.controller_process()
    ini_dict = ini_parsers.full_config(namespace.config)

    try:
        main(namespace.session, ini_dict['logging'])
    except:
        logger.exception('Exception in controller main.')
        raise
