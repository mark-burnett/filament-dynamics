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
import uuid

from . import database
from . import utils


# This is how we will identify this process to everyone.
UUID = str(uuid.uuid4())


def get_job():
    db_session = database.DBSession()
    job = db_session.query(database.Job).filter_by(complete=False,
            worker_uuid=None).with_lockmode('update_nowait').first()
    if job:
        job.worker_uuid = UUID
        db_session.commit()

    return job


def cleanup_incomplete_jobs():
    db_session = database.DBSession()
    job_query = db_session.query(database.Job).filter_by(complete=False
            ).filter(database.Job.worker_uuid != None)

    job_query.update({'worker_uuid': None})
    db_session.commit()
