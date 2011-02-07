#    Copyright (C) 2010 Mark Burnett
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
import configobj

import elixir

class DatabaseConfiguration(object):
    def __init__(self, server_type=None, username=None, password=None,
                 host=None, database_name=None):
        self.server_type = server_type
        self.username = username
        self.password = password
        self.host = host
        self.database_name = database_name

    @classmethod
    def from_configobj(cls, config):
        return cls(**config.get('database', {}))

    @property
    def bind(self):
        if not self.server_type:
            raise RuntimeError('Database server type not specified.')
        result = self.server_type + '://'
        if self.username and self.password and self.host:
            result += self.username + ':' + self.password
            result += '@' + self.host
        if not self.database_name:
            raise RuntimeError('Database name not specified.')
        result += '/' + self.database_name
        return result

def setup_database():
    ns, remaining_argv = parse_database_command_line()
    db_co = DatabaseConfiguration.from_configobj(
            configobj.ConfigObj(ns.config))
    elixir.metadata.bind = db_co.bind
    elixir.setup_all()

    return remaining_argv

def parse_database_command_line():
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', default='config.ini',
                        help='Configuration file name')

    return parser.parse_known_args()