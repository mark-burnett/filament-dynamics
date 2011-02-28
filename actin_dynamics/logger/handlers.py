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

from actin_dynamics import database
from actin_dynamics import job_control

class SQLAlachemyHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        self.db_session = database.DBSession()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        with self.db_session.transaction:
            lr = database.DBLogRecord.from_LogRecord(record)
            lr.process_id = job_control.PID
            self.db_session.add(lr)
