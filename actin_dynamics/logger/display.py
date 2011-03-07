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

import os.path

from . import colors

_default_color_scheme = {
        # Text colors
        'default':           {'foreground': colors.GREEN, 'bold': True},
        'message':           {'foreground': colors.WHITE},
        'filler':            {'foreground': colors.GREY},
        'time':              {'foreground': colors.GREY},
        'path':              {'foreground': colors.CYAN},
        'filename':          {'foreground': colors.GREEN},
        'exception_name':    {'foreground': colors.RED},
        'exception_message': {'foreground': colors.WHITE},
        'function_name':     {'foreground': colors.GREEN},
        'code':              {'foreground': colors.YELLOW},
        'line_number':       {'foreground': colors.CYAN},

        # Process types
        'worker':     {'foreground': colors.PURPLE},
        'controller': {'foreground': colors.YELLOW, 'bold': True},
        'test':       {'foreground': colors.BLUE, 'bold': True},

        # Logging levels
        'DEBUG':     {'foreground': colors.GREY},
        'INFO':      {'foreground': colors.YELLOW},
        'WARNING':   {'foreground': colors.YELLOW, 'bold': True},
        'ERROR':     {'foreground': colors.RED, 'bold': True},
        'CRITICAL':  {'background': colors.RED, 'bold': True},
        'EXCEPTION': {'background': colors.BLUE, 'bold': True}}

def _null_wrapper(text, *args, **kwargs):
    return text

def _null_clear():
    return ''

class LogDisplayer(object):
    def __init__(self, use_color=True, color_scheme=_default_color_scheme):
        if use_color:
            self._wrapper = colors.wrap
            self._clear   = colors.clear
        else:
            self._wrapper = _null_wrapper
            self._clear   = _null_clear

        self._filler_spec = color_scheme.get('filler', {})
        self.color_scheme = color_scheme

    def wrap(self, text, key=None):
        color_spec = self.color_scheme.get(key,
                self.color_scheme.get('default', {}))
        return self._wrapper(text, close=self._filler_spec, **color_spec)

    def clear(self):
        print self._clear(),

    def print_all(self, sequence):
        last_id = None
        for record in sequence:
            last_id = record.id
            self.print_record(record)
        return last_id

    def print_record(self, record):
        # Header
        #   log level, time, process type, process id
        if record.exception:
            log_level = 'EXCEPTION'
        else:
            log_level = record.levelname

        print '%s %s\tProcess type: %s, Process id: %s' % (
                self.wrap(log_level, log_level),
                self.wrap(record.time, 'time'),
                self.wrap(record.process.type,
                          record.process.type),
                self.wrap(record.process.id,
                          record.process.type))
        # Directory
        directory, filename = os.path.split(record.pathname)
        print "  Directory: '%s'" % self.wrap(directory, 'path')
        # File
        #   filename, line number, function name
        print "  File: '%s', Line %s, Function: '%s'" % (
                self.wrap(filename, 'filename'),
                self.wrap(record.lineno, 'line_number'),
                self.wrap(record.funcName, 'function_name'))
        # Message
        print '    %s' % self.wrap(record.message, 'message')
        # Exception
        if record.exception:
            self.print_exception(record.exception)
        # Clear
        self.clear()

    def print_exception(self, exception):
        print "  %s%s %s" % (self.wrap(exception.type_name, 'exception_name'),
                               self.wrap(':', 'filler'),
                               self.wrap(exception.message, 'exception_message'))

        self.print_traceback(exception.traceback)

    def print_traceback(self, traceback):
        for tbl in traceback:
            self._print_tb_level(tbl)
        print ''

    def _print_tb_level(self, tbl):
        print "%s\n  %s: %s" % (self.wrap(tbl.filename, 'filename'),
                                self.wrap(tbl.lineno,   'line_number'),
                                self.wrap(tbl.line,     'code'))
