#    Copyright (C) 2010 Mark Burnett
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

class MeasurementLabel(_elixir.Entity):
    _elixir.using_options(tablename='measurement_label')

    name = _elixir.Field(_elixir.Unicode(50), unique=True)
    description = _elixir.Field(_elixir.UnicodeText)
#    measurement_data = _elixir.OneToMany('MeasurementData')

    @classmethod
    def from_xml(cls, element):
        result = cls.get_by(name=unicode(element.get('name')))
        if not result:
            result = cls()
            result.name = unicode(element.get('name', None))
            result.description = unicode(element.get('description', None))
        return result
