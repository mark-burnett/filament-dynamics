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

import datetime as _datetime
import traceback as _traceback

from sqlalchemy import orm as _orm
from . import jobs as _jobs
from . import tables as _tables

class DBTraceback(object):
    def __init__(self, filename=None, lineno=None, module=None, line=None):
        if filename:
            self.filename = filename
        if lineno is not None:
            self.lineno = lineno
        if module:
            self.module = module
        if line:
            self.line = line

    def __repr__(self):
        return "%s(filename='%s', lineno=%s, module='%s', line='%s')" % (
                self.__class__.__name__, self.filename, self.lineno,
                self.module, self.line)

_orm.mapper(DBTraceback, _tables.traceback_table)

class DBException(object):
    def __init__(self, type=None, value=None, traceback=None, type_name=None,
                 message=None):
        if type:
            self.type_name = type.__name__
        if value:
            self.message = value.args[0]

        if type_name:
            self.type_name = type_name
        if message:
            self.message = message

        if traceback:
            self.traceback = []
            for line in _traceback.extract_tb(traceback):
                self.traceback.append(DBTraceback(*line))

    def __repr__(self):
        return "%s(type_name='%s', message='%s')" % (
                self.__class__.__name__, self.type_name, self.message)

_orm.mapper(DBException, _tables.exception_table, properties={
    'traceback': _orm.relationship(DBTraceback)})

class DBLogRecord(object):
    def __init__(self, name=None, pathname=None, funcName=None, lineno=None,
                 levelno=None, levelname=None, message=None, exception=None,
                 time=None):
        if name:
            self.name = name
        if pathname:
            self.pathname = pathname
        if funcName:
            self.funcName = funcName
        if lineno is not None:
            self.lineno = lineno

        if levelno is not None:
            self.levelno = levelno
        if levelname:
            self.levelname = levelname

        if message:
            self.message = message
        if exception:
            self.exception = exception

        if time:
            self.time = time

    def __repr__(self):
        return ("%s(name='%s', pathname='%s', funcName='%s', lineno=%s, "
                + "levelno=%s, levelname='%s', message='%s', time='%s')") % (
                    self.__class__.__name__, self.name, self.pathname,
                    self.funcName, self.lineno, self.levelno, self.levelname,
                    self.message, self.time)

    @classmethod
    def from_LogRecord(cls, log_record):
        dblr = cls()
        dblr.name      = log_record.name
        dblr.pathname  = log_record.pathname
        dblr.funcName  = log_record.funcName
        dblr.lineno    = log_record.lineno

        dblr.levelno   = log_record.levelno
        dblr.levelname = log_record.levelname

        dblr.message   = log_record.getMessage()
        dblr.exception = log_record.exc_info

        dblr.time      = _datetime.datetime.fromtimestamp(log_record.created)

        return dblr

    @property
    def exception(self):
        return self._exception

    @exception.setter
    def exception(self, value):
        if value:
            self._exception = DBException(*value)

_orm.mapper(DBLogRecord, _tables.logging_table, properties={
    '_exception': _orm.relationship(DBException, uselist=False),
    'process': _orm.relationship(_jobs.Process)})
