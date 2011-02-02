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

import elixir as _elixir

from . import mixins as _bases_classes
from . import parameters as _parameters

class Analysis(_elixir.Entity, _bases_classes.HasParameters):
    _elixir.using_options(tablename='analysis')

    parameters = _elixir.OneToMany('AnalysisParameter')
    values     = _elixir.OneToMany('AnalysisValue')

    run = _elixir.ManyToOne('Run')

    @classmethod
    def from_dicts(cls, parameter_dict=None, value_dict=None):
        analysis = cls()
        analysis.parameters = _parameters.AnalysisParameter.from_dict(
                parameter_dict)
        analysis.values = _parameters.AnalysisValue.from_dict(value_dict)

        return analysis
