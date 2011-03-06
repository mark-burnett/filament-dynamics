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

import argparse
import datetime

def _config(parser):
    parser.add_argument('-c', '--config', default='configuration/config.ini',
                        help='Configuration file name')
    return parser

def _session_file(parser):
    parser.add_argument('session', help='Session file name')
    return parser

def _delays_and_timeouts(parser):
    parser.add_argument('--idle_timeout', type=float, default=60,
                        help='Time to wait for a job to appear before quitting.')

    parser.add_argument('--retry_delay', type=float, default=5,
                        help='Time to wait on an empty queue before retry.')
    return parser

def _log_discriminators(parser):
    parser.add_argument('-t', '--time', action='store_true',
                        help='Filter results in time.')
    default_start_datetime = (datetime.datetime.now() -
                              datetime.timedelta(minutes=5))
    parser.add_argument('--start_time', default=str(default_start_datetime),
                        help='Show log events later than this.')
    parser.add_argument('--stop_time', default=None,
                        help="Don't show log entries later than this.")


    parser.add_argument('--min_level', type=int, default=None,
                        help='Show only log events of this level and higher (int).')

    parser.add_argument('--levelname', default=None,
                        help='Show only log events of this level.')


    parser.add_argument('--process_type', default=None,
                        help='Only report events from processes of this type.')

    parser.add_argument('--process_id', type=int, default=None,
                        help='Only report events from this process.')


    parser.add_argument('-f', '--follow', action='store_true',
                        help='Continue to report new events.')

    parser.add_argument('--polling_period', type=float, default=1,
                        help='Delay between database checks.')

    parser.add_argument('-n', '--nocolor', action='store_true',
                        help="Don't display colors.")

    return parser


def _build_and_execute_parser(functions):
    parser = argparse.ArgumentParser()
    for f in functions:
        parser = f(parser)
    return parser.parse_args()


_controller_args = [_config,
                    _session_file]

_worker_args     = [_config,
                    _delays_and_timeouts]

_db_util_args    = [_config]

_log_view_args   = [_config,
                    _log_discriminators]


def controller_process():
    return _build_and_execute_parser(_controller_args)

def worker_process():
    return _build_and_execute_parser(_worker_args)

def db_util():
    return _build_and_execute_parser(_db_util_args)

def view_log():
    return _build_and_execute_parser(_log_view_args)
