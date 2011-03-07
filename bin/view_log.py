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

import time
import datetime
import dateutil.parser

from actin_dynamics.configuration import command_line_parsers
from actin_dynamics.configuration import ini_parsers

from actin_dynamics import database

from actin_dynamics.logger import display


def make_query(last_id, start_time, stop_time, min_level, levelname,
               process_type, process_id, db_session):
    query = db_session.query(database.DBLogRecord)

    # Follow filter.
    if last_id:
        query = query.filter(database.DBLogRecord.id > last_id)

    # Logging filters.
    if levelname:
        query = query.filter_by(levelname=levelname)
    elif min_level is not None:
        query = query.filter(
                database.DBLogRecord.levelno >= min_level)

    # Process filters.
    if process_id is not None:
        query = query.filter_by(process_id=process_id)
    elif process_type:
        query = query.join(database.DBLogRecord.process
                ).filter(database.Process.type == process_type)

    # Time filters.
    if start_time:
        query = query.filter(database.DBLogRecord.time >= start_time)
    if stop_time:
        query = query.filter(database.DBLogRecord.time <= stop_time)

    return query


def main(filter_by_time=False, start_time=None, stop_time=None,
         min_level=None, level_name=None,
         process_type=None, process_id=None,
         follow=False, polling_period=None,
         use_color=True):

    disp = display.LogDisplayer(use_color=use_color)
    # NOTE We only need a read-only session.
    # I don't know whether SQLA supports that.
    if filter_by_time:
        start_time = dateutil.parser.parse(start_time)
        if stop_time:
            stop_time = dateutil.parser.parse(stop_time)
            if start_time > stop_time:
                start_time = None
    else:
        start_time = None
        stop_time  = None

    db_session = database.DBSession()

    with db_session.transaction:
        last_id = disp.print_all(make_query(0, start_time, stop_time,
                                            min_level, level_name,
                                            process_type, process_id,
                                            db_session))

    if follow:
        while True:
            if stop_time and datetime.datetime.now() > stop_time:
                break

            time.sleep(polling_period)
            with db_session.transaction:
                this_id = disp.print_all(make_query(last_id,
                                                    start_time, stop_time,
                                                    min_level, level_name,
                                                    process_type, process_id,
                                                    db_session))
            if this_id:
                last_id = this_id


if '__main__' == __name__:
    namespace = command_line_parsers.view_log()
    ini_parsers.setup_database(namespace.config)

    try:
        main(filter_by_time=namespace.time,
             start_time=namespace.start_time,
             stop_time=namespace.stop_time,
             min_level=namespace.min_level,
             level_name=namespace.levelname,
             process_type=namespace.process_type,
             process_id=namespace.process_id,
             follow=namespace.follow,
             polling_period=namespace.polling_period,
             use_color=not namespace.nocolor)
    except KeyboardInterrupt:
        pass # This is the normal halting path for follow mode.
