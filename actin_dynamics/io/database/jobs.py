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

class Job(_elixir.Entity, _mixins.GetOrCreate, _mixins.HasParameters):
    _elixir.using_options(tablename='job')

# XXX I can't use this until later versions of sqlalchemy.
#  This makes me wish I were using a rolling release distro like arch.
#    status = _elixir.Field(_elixir.Enum(['waiting', 'in progress', 'complete']))
    in_progress = _elixir.Field(_elixir.Boolean, default=False)
    complete    = _elixir.Field(_elixir.Boolean, default=False)

    parameters = _elixir.OneToMany('JobParameter')
    group      = _elixir.ManyToOne('Group')

#    @property
#    def parameters_dict(self):
#        return dict((p.name, p.value) for p in self.parameters)
#
#    def get_parameter(self, name):
#        return _parameters.JobParameter.query.filter_by(run=self,
#                name=name).first().value
