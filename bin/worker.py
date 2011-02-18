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

import time

from actin_dynamics.configuration import command_line_parsers
from actin_dynamics.configuration import database

from actin_dynamics import job_control, run_support

def main(idle_timeout, retry_delay):
    pass
#    time.sleep(delay)
#    for job in job_control.job_iterator():
#        run_support.run_simulation_job(job)
#        job_control.complete_job(job)


if '__main__' == __name__:
    namespace = command_line_parsers.worker_process()
    database.setup_database(namespace.db_config)

    main(namespace.idle_timeout, namespace.retry_delay)