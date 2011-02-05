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

from . import mixins as _mixins
from . import parameters as _parameters

class Job(_elixir.Entity, _mixins.HasParameters):
    _elixir.using_options(tablename='job')

    pid = _elixir.Field(_elixir.Integer, default=0)
    complete    = _elixir.Field(_elixir.Boolean, default=False)

    parameters = _elixir.OneToMany('JobParameter',
                                   cascade='all,delete,delete-orphan')
    group      = _elixir.ManyToOne('Group')

    @classmethod
    def from_parameters_dict(cls, parameters, group):
        return cls(group=group,
                   parameters=_parameters.JobParameter.from_dict(parameters))
