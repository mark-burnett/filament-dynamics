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

from actin_dynamics import database, io

def load_complete_session(filename, source_directory):
    session_dict = io.definitions.load_definition(filename, source_directory)

    experiments_dict = session_dict.get('experiments', {})
    model_dict = session_dict.get('model', {})

    parameter_generators_dict = session_dict.get('parameter_generators', {})

    name = session_dict.get('name', None)
    global_parameters = session_dict.get('global_parameters', {})

    session = database.Session(name=name, parameters=global_parameters)
