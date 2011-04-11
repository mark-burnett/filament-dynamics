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

import sqlalchemy.exceptions

from . import database

from . import logger
log = logger.getLogger(__file__)

def get_job(process_id, db_session):
    try:
        with db_session.transaction:
            job = db_session.query(database.Job).filter_by(stop_time=None,
                    worker_id=None).with_lockmode('update_nowait').first()
            if job:
                job.worker_id = process_id
                log.debug('Job acquired, id = %s.' % job.id)
            else:
                log.debug('No jobs found.')
    except sqlalchemy.exceptions.OperationalError as oe:
        # 1213 is the sqlalchemy deadlock warning number.
        if 1213 == oe.orig[0]:
            _log.warn('Deadlock while acquiring job %s.', job.id)
            job = None
        else:
            raise
    return job

def mark_job_complete(job, db_session):
    job.stop_time = datetime.datetime.now()
