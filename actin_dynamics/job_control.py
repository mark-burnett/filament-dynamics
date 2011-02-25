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

from . import database
from . import version


# This is how we will identify this process to everyone.
PROCESS = None


def register_process():
    global PROCESS
    if not PROCESS:
        rev, ctx = version.source_revision()
        PROCESS = database.Process(code_revision=rev, code_changeset=ctx,
                                   hostname=socket.gethostname(),
                                   uname=os.uname())
        db_session = database.DBSession()
        db_session.add(PROCESS)
        db_session.commit()

def unregister_process():
    global PROCESS
    if PROCESS:
        db_session = database.DBSession()
        db_session.add(PROCESS)
        PROCESS.stop_time = datetime.datetime.now()
        db_session.commit()

        PROCESS = None


def get_job():
    db_session = database.DBSession()
    job = db_session.query(database.Job).filter_by(complete=False,
            process_id=None).with_lockmode('update_nowait').first()
    if job:
        job.process = PROCESS
        db_session.commit()

    return job


# XXX This may need to delete partial data, like analyses or something.
def cleanup_incomplete_jobs():
    db_session = database.DBSession()
    job_query = db_session.query(database.Job).filter_by(complete=False
            ).filter(database.Job.process != None)

    job_query.update({'process': None})
    db_session.commit()
