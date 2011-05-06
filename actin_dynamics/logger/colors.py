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


CLEAR  = None
WHITE  = None
BLACK  = 30
RED    = 31
GREEN  = 32
YELLOW = 33
BLUE   = 34
PURPLE = 35
CYAN   = 36
GREY   = 37

ESCAPE_SEQUENCE = '\033['

def make_sequence(foreground=None, background=None, bold=False):
    if foreground:
        if bold:
            fg_sequence = '%s1;%sm' % (ESCAPE_SEQUENCE, foreground)
        else:
            fg_sequence = '%s%sm' % (ESCAPE_SEQUENCE, foreground)
    else:
        if bold:
            fg_sequence = '%s1m' % ESCAPE_SEQUENCE
        else:
            fg_sequence = ''

    if background:
        bg_sequence = '%s%sm' % (ESCAPE_SEQUENCE, (background + 10))
    else:
        bg_sequence = ''

    return '%s%s' % (bg_sequence, fg_sequence)

def clear():
    return '%sm' % ESCAPE_SEQUENCE


def wrap(text, foreground=None, background=None, bold=False, close={}):
    return "%s%s%s%s%s" % (clear(),
                         make_sequence(foreground=foreground,
                                       background=background, bold=bold),
                         text,
                         clear(),
                         make_sequence(**close))
