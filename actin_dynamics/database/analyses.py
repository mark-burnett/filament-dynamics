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

import itertools

from sqlalchemy import orm as _orm
from sqlalchemy.ext.associationproxy import association_proxy as _ap

from . import tables as _tables
from . import binds as _binds
from . import experiments as _experiments
from . import results as _results


class Analysis(object):
    def __init__(self, run=None, name=None, results=None):
        if run:
            self.run = run
        if name:
            self.name = name
        if results:
            self.results = results

    def __repr__(self):
        return "%s(run=%s, name='%s', results=%s)" % (
            self.__class__.__name__, self.run, self.name, self.results)

    @property
    def measurement(self):
        times  = []
        values = []
        errors = []
        for result in self.results:
            times.append(result.abscissa)
            values.append(result.ordinate)
            errors.append(result.error)

        return times, values, errors

    @measurement.setter
    def measurement(self, new_values):
        self.results = []
        for t, v, e in itertools.izip(*new_values):
            self.results.append(_results.AnalysisResult(abscissa=t,
                                                        ordinate=v,
                                                        error=e))

# Analysis should have binds
_orm.mapper(Analysis, _tables.analysis_table, properties={
    'results': _orm.relationship(_results.AnalysisResult, backref='analysis')})
