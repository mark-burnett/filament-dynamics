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

import socket
import os
import contextlib
import datetime
import itertools
import operator
import math

from sqlalchemy import sql

from . import database
from . import version

PID = None

_ZOMBIE_TIME = 1200
_WINDOW_TIME = 30

_process_type_map = {'controller': database.ControllerProcess,
                     'worker': database.WorkerProcess}

@contextlib.contextmanager
def process(process_type, db_session):
    '''
    Yields a process to be used for identifying work done.
    '''
    code_hash, code_modified  = version.source_version()
    process_cls = _process_type_map[process_type]
    p = process_cls(code_hash=code_hash, code_modified=code_modified,
                    hostname=socket.gethostname(), uname=os.uname())

    with db_session.transaction:
        db_session.add(p)

    # NOTE This just makes it easy to properly log the process.
    global PID
    PID = p.id

    try:
        yield p
    finally:
        with db_session.transaction:
            p.stop_time = datetime.datetime.now()


def close_zombie_processes(zombie_time=_ZOMBIE_TIME):
    db_session = database.DBSession()

    count = 0
    with db_session.transaction:
        zombie_processes = get_zombie_processes(db_session,
                zombie_time=zombie_time)
        for z in zombie_processes:
            z.stop_time = datetime.datetime.now()
            count += 1
    return count

def get_active_processes(db_session, zombie_time=_ZOMBIE_TIME):
    earliest_time = (datetime.datetime.now() -
                     datetime.timedelta(seconds=zombie_time))
    q = db_session.query(database.WorkerProcess
            ).filter_by(stop_time=None
            ).filter(sql.or_(
                database.WorkerProcess.jobs.any(
                    database.Job.start_time > earliest_time),
                database.WorkerProcess.start_time > earliest_time))
    return q

def get_zombie_processes(db_session, zombie_time=_ZOMBIE_TIME):
    earliest_time = (datetime.datetime.now() -
                     datetime.timedelta(seconds=zombie_time))
    q = db_session.query(database.WorkerProcess
            ).filter_by(stop_time=None
            ).filter(sql.not_(sql.or_(database.WorkerProcess.jobs.any(
                database.Job.start_time > earliest_time),
                database.WorkerProcess.start_time > earliest_time)))
    return q

def get_closed_processes(db_session, newer_than=None):
    q = db_session.query(database.WorkerProcess
            ).filter(database.Process.stop_time != None)
    if newer_than:
        q = q.filter(database.Process.start_time > newer_than)
    return q

def get_completed_jobs(db_session, process):
    q = db_session.query(database.Job).filter_by(worker=process
            ).filter(database.Job.stop_time != None)
    return q

def get_most_recent_job(db_session, process):
    q = db_session.query(database.Job).filter_by(worker=process
            ).order_by(database.Job.start_time.desc())
    return q.first()


def estimate_runtime(db_session, zombie_time=_ZOMBIE_TIME,
        window_time=_WINDOW_TIME):
    # Get active processes
    active_processes = get_active_processes(db_session, zombie_time=zombie_time
            ).order_by(database.WorkerProcess.start_time)

    # Get closed processes newer than oldest active process - window time
    oldest_active = active_processes.first()
    oldest_time = oldest_active.start_time - datetime.timedelta(window_time)
    closed_processes = get_closed_processes(db_session, newer_than=oldest_time)

    # Calculate average time/job based on all those processes
    times = get_process_job_times(itertools.chain(active_processes,
                                                  closed_processes))
    if not times:
        return 'Unknown'

    average = reduce(operator.add, times) / len(times)

    # Get active jobs
    active_process_count = active_processes.count()
    active_jobs = [get_most_recent_job(db_session, p) for p in active_processes]

    active_times = get_job_times(active_jobs)
    active_complete = reduce(operator.add, active_times,
            datetime.timedelta()) / active_process_count
    active_remaining = max(active_complete - average, datetime.timedelta())

    # Get remaining jobs
    inactive_job_count = db_session.query(database.Job).filter_by(
            start_time=None).count()

    # Round robin calculation to see how much time is left
    inactive_time = int(math.ceil(inactive_job_count / active_process_count))
    inactive_time *= average
    return active_remaining + inactive_time


def get_process_job_times(processes):
    times = []
    for p in processes:
        times.extend(get_job_times(p.jobs))
    return times

def get_job_times(jobs):
    return [j.stop_time - j.start_time for j in jobs if j.stop_time]
