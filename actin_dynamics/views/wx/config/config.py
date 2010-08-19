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

from .border_config import wxBorderConfig as _wxBorderConfig
from .font_config import wxFontConfig as _wxFontConfig
from .sizer_config import wxSizerConfig as _wxSizerConfig
from .style_config import wxStyleConfig as _wxStyleConfig

class wxConfigObject(object):
    def __init__(self, window_size=None, border=None, style=None, sizer=None,
                 font=None):
        self.window_size = window_size

        self.border = border
        self.style = style
        self.sizer = sizer
        self.font = font

    @classmethod
    def from_configobj(cls, config):
        window_size = tuple(map(int, config.get('window_size', tuple())))

        font_config = config.get('font', {})
        font_object = _wxFontConfig.from_configobj(font_config)

        border_config = config.get('border', {})
        border_object = _wxBorderConfig.from_configobj(border_config)

        style_config = config.get('style', {})
        style_object = _wxStyleConfig.from_configobj(style_config)

        sizer_config = config.get('sizer', {})
        sizer_object = _wxSizerConfig.from_configobj(sizer_config)

        return cls(font=font_object, window_size=window_size,
                   sizer=sizer_object, border=border_object,
                   style=style_object)
