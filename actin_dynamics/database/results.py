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

class _Data(object):
    def __init__(self, abscissa=None, ordinate=None, error=None):
        if abscissa is not None:
            self.abscissa = abscissa
        if ordinate is not None:
            self.ordinate = ordinate
        if error is not None:
            self.error = error

    def __repr__(self):
        return '%s(abscissa=%s, ordinate=%s, error=%s)' % (
                self.__class__.__name__, self.abscissa, self.ordinate,
                self.error)

class AnalysisResult(_Data): pass

_orm.mapper(AnalysisResult, _tables.analysis_results_table)

class ObjectiveData(_Data): pass

_orm.mapper(ObjectiveData, _tables.objective_data_table)
