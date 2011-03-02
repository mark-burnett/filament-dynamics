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

from actin_dynamics.io import definitions
from . import database

from actin_dynamics import logger

log = logger.getLogger(__file__)

def load_complete_session(db_session, filename):
    session_dict = definitions.load_definition(filename)
    name = session_dict.get('name', None)
    log.debug("Loading session: '%s'." % name)

    experiments_dict = session_dict.get('experiments', {})
    log.debug('Found %s experiment definitions.' % len(experiments_dict))

    model_dict = session_dict.get('models', {})
    log.debug('Found %s model definitions.' % len(model_dict))

    global_parameters = session_dict.get('global_parameters', {})
    log.debug('Found %s global parameters.' % len(global_parameters))

    par_spec_dict = session_dict.get('parameter_specifications', {})
    session = database.create_static_session(db_session, name=name,
            parameters=global_parameters, model=model_dict,
            experiments=experiments_dict,
            parameter_specifications=par_spec_dict)

    parameter_specifications_dict = session_dict.get(
            'parameter_specifications', {})
    log.debug('Found %s parameter specifications.' % len(
        parameter_specifications_dict))

    return session, parameter_specifications_dict
