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

import logging
from actin_dynamics.logger import handlers

def setup_logging_from_dict(log_dict):
    root_logger = logging.getLogger()

    levelname = log_dict.get('level', 'WARN')
    level = getattr(logging, levelname)
    root_logger.setLevel(level)

    root_logger.addHandler(handlers.SQLAlachemyHandler())
