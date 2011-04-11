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
from actin_dynamics.configuration import logger as logger_config

from actin_dynamics import job_control, run_support, database, process_control

logger = logging.getLogger()


def main(idle_timeout, retry_delay, log_dict):
    db_session = database.DBSession()
    with process_control.process('worker', db_session) as process:
        logger_config.setup_logging_from_dict(log_dict)
        stop_time = time.time() + idle_timeout
        while time.time() < stop_time:
            job = job_control.get_job(process.id, db_session)
            if job:
                with db_session.transaction:
                    run_support.run_job(job, db_session)
                    run_support.mark_job_complete(job, db_session)
                stop_time = time.time() + idle_timeout
            else:
                time.sleep(retry_delay)


if '__main__' == __name__:
    namespace = command_line_parsers.worker_process()
    ini_dict = ini_parsers.full_config(namespace.config)

    try:
        main(namespace.idle_timeout, namespace.retry_delay,
             ini_dict['logging'])
    except:
        logger.exception('Exception in worker main.')
        raise
