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
from . import logs as _logs
from . import jobs as _jobs

class Process(object):
    def __init__(self, code_changeset=None, hostname=None, uname=None):
        if code_changeset:
            self.code_changeset = code_changeset
        if hostname:
            self.hostname = hostname
        if uname:
            self.uname = uname

    def __repr__(self):
        return ("%s(code_changeset='%s', hostname='%s', uname=%s, " +
                "start_time=%s, stop_time=%s)") % (
                self.__class__.__name__, self.code_changeset,
                self.hostname, self.uname, self.start_time, self.stop_time)

    @property
    def uname(self):
        return (self.sysname, self.nodename, self.release, self.version,
                self.machine)

    @uname.setter
    def uname(self, new_value):
        (self.sysname, self.nodename, self.release, self.version,
                self.machine) = new_value

_process_mapper = _orm.mapper(Process, _tables.process_table,
        polymorphic_on=_tables.process_table.c.type, properties={
    'log_entries': _orm.relationship(_logs.DBLogRecord, backref='process',
        cascade='all,delete-orphan')})

class ControllerProcess(Process): pass

_orm.mapper(ControllerProcess, inherits=_process_mapper, properties={
    'jobs': _orm.relationship(_jobs.Job, backref='creator',
        primaryjoin=_tables.job_table.c.creator_id==_tables.process_table.c.id,
        cascade='all,delete-orphan')},
    polymorphic_identity='controller')

class WorkerProcess(Process): pass

_orm.mapper(WorkerProcess, inherits=_process_mapper, properties={
    'jobs': _orm.relationship(_jobs.Job, backref='worker',
        primaryjoin=_tables.job_table.c.worker_id==_tables.process_table.c.id,
        cascade='all,delete-orphan')},
    polymorphic_identity='worker')
