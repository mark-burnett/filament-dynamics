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

from . import analyses
from . import tables

__all__ = ['Run']

class Run(object):
    def __init__(self, parameter_set=None, experiment=None, analyses=None):
        if parameter_set:
            self.parameter_set = parameter_set
        if experiment:
            self.experiment = experiment

        if analyses:
            self.analyses = analyses

    def __repr__(self):
        return "%s(id=%s, parameter_set_id=%s, experiment_id=%s)" % (
            self.__class__.__name__, self.id, self.parameter_set_id,
            self.experiment_id)


orm.mapper(Run, tables.run_table, properties={
    'analyses': orm.relationship(analyses.Analysis, backref='run',
        cascade='all,delete-orphan')})
