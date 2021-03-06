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
import datetime
import socket
import os

import contextlib

import sqlalchemy.exc

from . import database
from . import version

from . import logger

log = logger.getLogger(__file__)

PID = None

@contextlib.contextmanager
def process(process_type, db_session):
    '''
    Yields a process to be used for identifying work done.
    '''
    ctx = version.source_hash()
    p = database.Process(code_changeset=ctx,
                         hostname=socket.gethostname(),
                         uname=os.uname(), type=process_type)

    with db_session.transaction:
        db_session.add(p)

    # NOTE This just makes it easy to properly log the process.
    global PID
    PID = p.id
    log.info('Registered process %s as %s.' % (p.id, p.type))

    yield p

    # Rollback, to make sure an exception doesn't block unregistering.
    with db_session.transaction:
        p.stop_time = datetime.datetime.now()
    log.info('Unegistered process %s.' % p.id)


def get_job(process_id, db_session):
    try:
        with db_session.transaction:
            maybe_job = db_session.query(database.Job).filter_by(complete=False,
                    worker_id=None).with_lockmode('update_nowait')
            if maybe_job:
                job = maybe_job.first()
                if job:
                    job.worker_id = process_id
                    log.debug('Job acquired, id = %s.' % job.id)
                else:
                    log.debug('No jobs found.')
            else:
                log.warn('Job query failed to return rows.')
    except sqlalchemy.exc.OperationalError as oe:
        if 1213 == oe.orig[0]:
            log.warn('Deadlock while acquiring job %s.', job.id)
            job = None
        else:
            raise
    return job


# XXX This may need to delete partial data, like analyses or something.
# XXX Fix session management
def restart_incomplete_jobs():
    db_session = database.DBSession()
    with db_session.transaction:
        job_query = db_session.query(database.Job).filter_by(complete=False
                ).filter(database.Job.worker_id != None)

        job_query.update({'worker_id': None})

def delete_jobs():
    db_session = database.DBSession()
    with db_session.transaction:
        job_query = db_session.query(database.Job).filter_by(complete=False)
        job_query.update({'complete': True})


def job_status():
    db_session = database.DBSession()
    with db_session.transaction:
        incomplete_count = db_session.query(database.Job
                ).filter_by(complete=False).count()
        assigned_count = db_session.query(database.Job
                ).filter_by(complete=False).filter(database.Job.worker != None
                ).count()
        unassigned_count = db_session.query(database.Job
                ).filter_by(complete=False).filter_by(worker=None).count()
    print
    print 'Incomplete jobs:', incomplete_count
    print 'Assigned jobs:', assigned_count
    print 'Unassigned jobs:', unassigned_count
