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

from sqlalchemy import sql

from . import database
from . import version

PID = None

_ZOMBIE_TIME = 1200

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

    yield p

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
            ).filter(sql.not_(database.WorkerProcess.jobs.any(
                database.Job.start_time > earliest_time)))
    return q

def get_closed_processes(db_session):
    q = db_session.query(database.WorkerProcess
            ).filter(database.Process.stop_time != None)
    return q

def get_completed_jobs(db_session, process):
    q = db_session.query(database.Job).filter_by(worker=process
            ).filter(database.Job.stop_time != None)
    return q

def get_most_recent_job(db_session, process):
    q = db_session.query(database.Job).filter_by(worker=process
            ).order_by(database.Job.start_time.desc())
    return q.first()
