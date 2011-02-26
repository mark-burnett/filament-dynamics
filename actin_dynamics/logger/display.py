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

from . import colors

def print_all(seq):
    for record in seq:
        print_record(record)

log_colors = {
    'DEBUG':    lambda t: colors.wrap(t, foreground=colors.GREY),
    'INFO':     lambda t: colors.wrap(t, foreground=colors.CYAN),
    'WARNING':  lambda t: colors.wrap(t, foreground=colors.YELLOW, bold=True),
    'ERROR':    lambda t: colors.wrap(t, foreground=colors.RED, bold=True),
    'CRITICAL': lambda t: colors.wrap(t, background=colors.RED, bold=True)}

def _get_level_text(record):
    return log_colors[record.levelname](record.levelname)

def print_record(record):
    header =\
'''%s @ %s
    Process type: %s, Process id: %s
    File: '%s', line %s
    Function: '%s'
        %s''' % (_get_level_text(record),
       colors.wrap(record.time, foreground=colors.YELLOW),
       colors.wrap(record.process.type, foreground=colors.PURPLE),
       colors.wrap(record.process.id, foreground=colors.PURPLE),
       colors.wrap(record.pathname, foreground=colors.CYAN),
       colors.wrap(record.lineno, foreground=colors.CYAN),
       colors.wrap(record.funcName, foreground=colors.CYAN),
       colors.wrap(record.message, foreground=colors.GREEN))

    print header

    if record.exception:
        print_exception(record.exception)

def print_exception(exception):
    header =\
'''    %s: %s
       %s''' % (
       colors.wrap('Exception', background=colors.BLUE, bold=True),
       colors.wrap(exception.type_name, foreground=colors.RED),
       colors.wrap(exception.message, foreground=colors.GREEN))

    print header

    print_traceback(exception.traceback)

def print_traceback(traceback):
    print '    %s:' % colors.wrap('Traceback', foreground=colors.BLACK, bold=True)
    for tbl in traceback:
        print_tb_level(tbl)
    print ''

def print_tb_level(tbl):
    text =\
'''        File: '%s'
%s: %s''' % (colors.wrap(tbl.filename, foreground=colors.CYAN),
       colors.wrap(tbl.lineno, foreground=colors.CYAN),
       colors.wrap(tbl.line, foreground=colors.YELLOW))

    print text
