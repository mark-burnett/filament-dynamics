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


from sqlalchemy import orm as _orm

from . import tables as _tables
from . import binds as _binds


class Model(object): pass

_orm.mapper(Model, _tables.model_table, properties={
    'binds': _orm.relationship(_binds.Bind,
        secondary=_tables.model_bind_table),
    'concentrations': _orm.relationship(_binds.ConcentrationBind,
        secondary=_tables.model_bind_table),
    'transitions': _orm.relationship(_binds.TransitionBind,
        secondary=_tables.model_bind_table)})
