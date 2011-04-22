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


from sqlalchemy import orm

from . import tables
from . import parameters

__all__ = ['Objective']

class Objective(object):
    def __init__(self, run=None, binding=None, value=None):
        if run:
            self.run = run
        if binding:
            self.binding = binding
        if value is not None:
            self.value = value

    def __repr__(self):
        return "%s(id=%s, run_id=%s, binding_id=%s, value=%s)" % (
            self.__class__.__name__, self.id, self.run_id, self.binding_id,
            self.value)


orm.mapper(Objective, tables.objective_table)
