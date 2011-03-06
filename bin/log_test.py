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
import time

from actin_dynamics.configuration import command_line_parsers
from actin_dynamics.configuration import ini_parsers

from actin_dynamics import job_control, run_support, database

logger = logging.getLogger()

def foo_raises():
    raise RuntimeError('Test exception.')

def main():
    db_session = database.DBSession()
    with job_control.process('test', db_session) as process:
        logger.debug('Test debug message.')
        logger.info('Test info message.')
        logger.warn('Test warn message.')
        logger.error('Test error message.')
        logger.critical('Test critical message.')
        try:
            foo_raises()
        except:
            logger.exception('Apparently I can catch exceptions too!')


if '__main__' == __name__:
    namespace = command_line_parsers.worker_process()
    ini_parsers.full_config(namespace.config)

    main()
