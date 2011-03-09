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

class Process(object):
    def __init__(self, type=None, code_revision=None, code_changeset=None,
                 hostname=None, uname=None):
        if type:
            self.type = type
        if code_revision:
            self.code_revision = code_revision
        if code_changeset:
            self.code_changeset = code_changeset
        if hostname:
            self.hostname = hostname
        if uname:
            self.uname = uname

    def __repr__(self):
        return ("%s(type='%s', code_revision=%s, code_changeset='%s', "
                + "hostname='%s', uname=%s, start_time=%s, stop_time=%s)") % (
                self.__class__.__name__, self.type,
                self.code_revision, self.code_changeset,
                self.hostname, self.uname, self.start_time, self.stop_time)

    @property
    def uname(self):
        return (self.sysname, self.nodename, self.release, self.version,
                self.machine)

    @uname.setter
    def uname(self, new_value):
        (self.sysname, self.nodename, self.release, self.version,
                self.machine) = new_value

_orm.mapper(Process, _tables.process_table)


class Job(object):
    def __init__(self, run=None, worker=None, creator=None, complete=None):
        if run:
            self.run = run
        if worker:
            self.worker = worker
        if creator:
            self.creator = creator
        if complete is not None:
            self.complete = complete

    def __repr__(self):
        return ("%s(id=%s, run_id=%s, worker_id=%s, creator_id=%s, complete=%s)"
                % (self.__class__.__name__, self.id, self.run_id,
                   self.worker_id, self.creator_id, self.complete))

_orm.mapper(Job, _tables.job_table, properties={
    'run': _orm.relationship(_runs.Run, backref='job'),
    'worker': _orm.relationship(Process,
        primaryjoin=_tables.job_table.c.worker_id==_tables.process_table.c.id),
    'creator': _orm.relationship(Process,
        primaryjoin=_tables.job_table.c.creator_id==_tables.process_table.c.id)})
