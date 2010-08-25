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

class ParameterLabel(_elixir.Entity):
    _elixir.using_options(tablename='parameter_label')

    name = _elixir.Field(_elixir.Unicode(50), unique=True)
    description = _elixir.Field(_elixir.UnicodeText)

    @classmethod
    def from_xml(cls, element):
        result = cls.get_by(name=element.get('name'))
        if not result:
            result = cls()
            result.from_dict(element.attrib)
        return result


