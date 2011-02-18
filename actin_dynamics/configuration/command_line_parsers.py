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

def _database_config(args, namespace):
    parser = argparse.ArgumentParser()

    parser.add_argument('--db_config', default='configuration/database.ini',
                        help='Databsae configuration file name')

    return parser.parse_known_args(args=args, namespace=namespace)

def _delays_and_timeouts(args, namespace):
    parser = argparse.ArgumentParser()

    parser.add_argument('--idle_timeout', type=float, default=120,
                        help='Time to wait for a job to appear before quitting.')

    parser.add_argument('--retry_delay', type=float, default=5,
                        help='Time to wait on an empty queue before retry.')

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


_worker_args = [_database_config,
                _delays_and_timeouts]
#                _catch_extra_arguments]

_db_util_args = [_database_config]
#                 _catch_extra_arguments]


def worker_process():
    return execute_parser_list(_worker_args)

def db_util():
    return execute_parser_list(_db_util_args)
