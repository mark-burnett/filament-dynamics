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

class Job(object):
    def __init__(self, run=None, worker=None, creator=None,
                 start_time=None, stop_time=None):
        if run:
            self.run = run
        if worker:
            self.worker = worker
        if creator:
            self.creator = creator
        if start_time:
            self.start_time = start_time
        if stop_time:
            self.stop_time = stop_time

    def __repr__(self):
        return ("%s(id=%s, run_id=%s, worker_id=%s, creator_id=%s, "
                + "start_time='%s', stop-time='%s')"
                % (self.__class__.__name__, self.id, self.run_id,
                   self.worker_id, self.creator_id,
                   self.start_time, self.stop_time))

_orm.mapper(Job, _tables.job_table)
