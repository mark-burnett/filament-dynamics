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

class GetOrCreate(object):
    @classmethod
    def get_or_create(cls, *args, **kwargs):
        result = cls.get_by(*args, **kwargs)
        if result:
            return result
        return cls(*args, **kwargs)


class HasParameters(object):
    @property
    def parameters_dict(self):
        return dict((p.name, p.value) for p in self.parameters)

    def get_parameter(self, name):
        for p in self.parameters:
            if p.name == name:
                return p.value
