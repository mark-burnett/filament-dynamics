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


from sqlalchemy import orm as _orm

from . import tables as _tables
from . import runs as _runs

class Job(object):
    def __init__(self, run=None, worker_uuid=None, complete=None):
        if run:
            self.run = run
        if worker_uuid:
            self.worker_uuid = worker_uuid
        if complete is not None:
            self.complete = complete

    def __repr__(self):
        return "%s(run=%s, worker_uuid=%s, complete=%s)" % (
                self.__class__.__name__, self.run,
                self.worker_uuid, self.complete)

_orm.mapper(Job, _tables.job_table, properties={
    'run': _orm.relationship(_runs.Run)})
