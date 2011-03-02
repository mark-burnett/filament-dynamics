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

import sqlalchemy.exceptions

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
    rev, ctx = version.source_revision()
    p = database.Process(code_revision=rev, code_changeset=ctx,
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
            job = db_session.query(database.Job).filter_by(complete=False,
                    worker_id=None).with_lockmode('update_nowait').first()
            if job:
                job.worker_id = process_id
                log.debug('Job acquired, id = %s.' % job.id)
            else:
                log.debug('No jobs found.')
    except sqlalchemy.exceptions.OperationalError as oe:
        if 1213 == oe.orig[0]:
            _log.warn('Deadlock while acquiring job %s.', job.id)
            job = None
        else:
            raise
    return job


# XXX This may need to delete partial data, like analyses or something.
# XXX Fix session management
def cleanup_incomplete_jobs():
    db_session = database.DBSession()
    job_query = db_session.query(database.Job).filter_by(complete=False
            ).filter(database.Job.worker != None)

    job_query.update({'worker': None})
    db_session.commit()
