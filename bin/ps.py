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

import datetime

from actin_dynamics.configuration import command_line_parsers
from actin_dynamics.configuration import ini_parsers

from actin_dynamics import database, process_control

from actin_dynamics.logger import colors

def display_zombie_process(db_session, process):
    last_job = process_control.get_most_recent_job(db_session, process)
    if last_job:
        if last_job.stop_time:
            recent_time = last_job.stop_time
        else:
            recent_time = last_job.start_time
    else:
        recent_time = process.start_time
    zombie_time = datetime.datetime.now() - recent_time

    jobs = process_control.get_completed_jobs(db_session, process)

    print colors.wrap('%s %s completed %s jobs, zombie for %s' % (
            process.type, process.id, jobs.count(), zombie_time),
            foreground=colors.BLACK, bold=True)

def display_live_process(db_session, process):
    jobs = process_control.get_completed_jobs(db_session, process)
    alive_time = datetime.datetime.now() - process.start_time

    print colors.wrap('%s %s completed %s jobs in %s' % (
            process.type, process.id, jobs.count(), alive_time),
            foreground=colors.GREEN)

def main(live_timeout):
    db_session = database.DBSession()

    zombies = process_control.get_zombie_processes(db_session, live_timeout)

    live = process_control.get_active_processes(db_session, live_timeout)

    for p in process_control.get_zombie_processes(db_session, live_timeout):
        display_zombie_process(db_session, p)

    for p in process_control.get_active_processes(db_session, live_timeout):
        display_live_process(db_session, p)

    # Remaining time estimate
#    if db_session.query(database.Job).filter_by(stop_time=None).count():
#        print
#        print process_control.get_runtime_estimate(db_session, live_timeout)


if '__main__' == __name__:
    namespace = command_line_parsers.process_utils()
    ini_parsers.full_config(namespace.config)

    main(live_timeout=namespace.live_timeout)
