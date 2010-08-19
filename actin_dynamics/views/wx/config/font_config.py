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

class wxFontConfig(object):
    def __init__(self, default_font_family, default_font_size, font_definitions):
        self.default_font_family = default_font_family
        self.default_font_size = default_font_size
        self.font_definitions = font_definitions

    def __call__(self, name):
         return self.make_font(**self.font_definitions.get(name, {}))

    @classmethod
    def from_configobj(cls, font_config):
        default_family_text = font_config.get('default_family', 'DEFAULT')
        default_family = getattr(_wx,
                                 'FONTFAMILY_' + default_family_text.upper())

        default_size = int(font_config.get('default_size', 12))

        font_definitions = {}
        for section_name in font_config.sections:
            font_definitions[section_name] = font_config[section_name]

        return cls(default_font_family=default_family,
                   default_font_size=default_size,
                   font_definitions=font_definitions)

    def make_font(self, family=None, size=None, italic=False, bold=False,
                  light=False, underline=False, strikethrough=False,
                  slant=False, weight=None):
        if family:
            font_family = getattr(_wx, 'FONTFAMILY_' + family.upper())
        else:
            font_family = self.default_font_family

        if size:
            font_size = int(size)
        else:
            font_size = self.default_font_size

        style = 0
        if italic:
            style = style | _wx.FONTFLAG_ITALIC
        if bold:
            style = style | _wx.FONTFLAG_BOLD
        if light:
            style = style | _wx.FONTFLAG_LIGHT
        if underline:
            style = style | _wx.FONTFLAG_UNDERLINED
        if strikethrough:
            style = style | _wx.FONTFLAG_STRIKETHROUGH
        if slant:
            style = style | _wx.FONTFLAG_SLANT

        if not style:
            sytle = _wx.FONTFLAG_DEFAULT

        if weight is not None:
            font_weight = _utils.get_flags(weight, prefix='FONTWEIGHT_',
                                           module=_wx)
        else:
            font_weight = _wx.FONTWEIGHT_NORMAL

        return _wx.Font(font_size, family=font_family,
                        style=style, weight=font_weight)
