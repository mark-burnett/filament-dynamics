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

import configobj

from . import database

def full_config(filename):
    co = configobj.ConfigObj(filename)
    database.setup_database_from_dict(co['database'])
    return co

def setup_database(config_filename):
    '''Uses config file to create database access singletons.
    '''
    co = configobj.ConfigObj(config_filename)
    database.setup_database_from_dict(co['database'])
