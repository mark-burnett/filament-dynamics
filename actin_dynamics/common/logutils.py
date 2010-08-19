#    Copyright (C) 2010 Mark Burnett, David Morton
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

import os
import logging

TOP_NAME = 'actin_dynamics'

def getLogger(filename):
    long_name, junk = os.path.splitext(filename)
    begining, end = os.path.split(long_name)
    logger_name = ''
    while not (TOP_NAME == end or '' == end):
        logger_name = '.' +  end + logger_name
        begining, end = os.path.split(begining)
    else:
        logger_name = end + logger_name

    return logging.getLogger(logger_name)

