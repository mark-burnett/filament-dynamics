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

g = lambda t: colors.wrap(t, foreground=colors.GREY)

def print_all(seq):
    for record in seq:
        print_record(record)

_log_colors = {
    'DEBUG':     lambda t: colors.wrap(t, foreground=colors.GREY),
    'INFO':      lambda t: colors.wrap(t, foreground=colors.YELLOW),
    'WARNING':   lambda t: colors.wrap(t, foreground=colors.YELLOW, bold=True),
    'ERROR':     lambda t: colors.wrap(t, foreground=colors.RED, bold=True),
    'CRITICAL':  lambda t: colors.wrap(t, background=colors.RED, bold=True),
    'EXCEPTION': lambda t: colors.wrap(t, background=colors.BLUE, bold=True)}

def _get_level_text(record):
    if record.exception:
        return _log_colors['EXCEPTION']('EXCEPTION')
    return _log_colors[record.levelname](record.levelname)

_proc_colors = {
    'worker':     lambda t: colors.wrap(t, foreground=colors.PURPLE),
    'controller': lambda t: colors.wrap(t, foreground=colors.YELLOW, bold=True)}

def _get_process_text(record):
    wrapper = _proc_colors.get(record.process.type.lower(),
            lambda t: colors.wrap(t, foreground=colors.BLUE, bold=True))
    text = "%s %s%s %s" % (g('Process type:'), wrapper(record.process.type),
                           g(', Process id:'), wrapper(record.process.id))
    return text

def print_record(record):
    directory, filename = os.path.split(record.pathname)
    header =\
'''%s %s    %s
  %s%s%s
  %s%s%s %s%s%s%s
      %s''' % (_get_level_text(record), g(record.time),
       _get_process_text(record),

       g("Directory: '"),
       colors.wrap(directory, foreground=colors.CYAN),
       g("'"),

       g("File: '"),
       colors.wrap(filename, foreground=colors.GREEN),
       g("', Line"),
       colors.wrap(record.lineno, foreground=colors.GREEN),
       g(", Function: '"),
       colors.wrap(record.funcName, foreground=colors.GREEN),
       g("'"),
       record.message)

    print header

    if record.exception:
        print_exception(record.exception)

def print_exception(exception):
    header = "  %s%s %s" % (
       colors.wrap(exception.type_name, foreground=colors.RED),
       g(':'), exception.message)

    print header

    print_traceback(exception.traceback)

def print_traceback(traceback):
    for tbl in traceback:
        print_tb_level(tbl)
    print ''

def print_tb_level(tbl):
    text = "%s%s%s\n  %s: %s" % (
            g("'"),
            colors.wrap(tbl.filename, foreground=colors.GREEN),
            g("'"),
            colors.wrap(tbl.lineno, foreground=colors.CYAN),
            colors.wrap(tbl.line, foreground=colors.YELLOW))
    print text
