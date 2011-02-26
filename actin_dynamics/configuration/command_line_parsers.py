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
import sys

# XXX This could be improved so that we give the correct help message.

def _config(args, namespace):
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', default='configuration/config.ini',
                        help='Configuration file name')

    return parser.parse_known_args(args=args, namespace=namespace)

def _delays_and_timeouts(args, namespace):
    parser = argparse.ArgumentParser()

    parser.add_argument('--idle_timeout', type=float, default=120,
                        help='Time to wait for a job to appear before quitting.')

    parser.add_argument('--retry_delay', type=float, default=5,
                        help='Time to wait on an empty queue before retry.')

    return parser.parse_known_args(args=args, namespace=namespace)

def _log_discriminators(args, namespace):
    parser = argparse.ArgumentParser()

    parser.add_argument('--start', default=None,
                        help='Show log events later than this.')


    parser.add_argument('--min_level', default=None,
                        help='Show only log events of this level and higher.')

    parser.add_argument('--levelname', default=None,
                        help='Show only log events of this level.')


    parser.add_argument('--process_type', default=None,
                        help='Only report events from processes of this type.')

    parser.add_argument('--process_id', type=int, default=None,
                        help='Only report events from this process.')


    parser.add_argument('--follow', type=bool, default=False,
                        help='Show only log events of this level.')

    parser.add_argument('--polling_period', type=float, default=1,
                        help='Delay between database checks.')

    return parser.parse_known_args(args=args, namespace=namespace)


def _catch_extra_arguments(args, namespace):
    parser = argparse.ArgumentParser()
    return parser.parse_args(args=args, namespace=namespace)


def execute_parser_list(functions):
    namespace = argparse.Namespace()
    remaining_args = sys.argv
    for f in functions:
        junk_namespace, remaining_args = f(remaining_args, namespace)

    return namespace


_worker_args = [_config,
                _delays_and_timeouts]
#                _catch_extra_arguments]

_db_util_args = [_config]
#                 _catch_extra_arguments]

_log_view_args = [_config,
                  _log_discriminators]

def worker_process():
    return execute_parser_list(_worker_args)

def db_util():
    return execute_parser_list(_db_util_args)

def view_log():
    return execute_parser_list(_log_view_args)
