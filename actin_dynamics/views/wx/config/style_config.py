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

import wx as _wx

from . import utils as _utils

class wxStyleConfig(object):
    def __init__(self, style_definitions):
        self.style_definitions = style_definitions

    def __call__(self, name):
        return self.style_definitions[name]

    @classmethod
    def from_configobj(cls, config):
        style_definitions = {}
        for name, value in config.iteritems():
            style_definitions[name] = _utils.get_flags(value, module=_wx)

        return cls(style_definitions)
