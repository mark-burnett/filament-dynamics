#!/usr/bin/env python

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

from actin_dynamics.configuration import command_line_parsers
from actin_dynamics.configuration import database

from actin_dynamics import job_control

def cleanup_jobs():
    job_control.cleanup_jobs()


if '__main__' == __name__:
    namespace = command_line_parsers.worker_process()
    database.setup_database(namespace.db_config)

    cleanup_jobs()
