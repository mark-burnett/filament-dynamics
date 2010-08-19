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

import wx

from .elements_panel import ElementsPanel
from .selection_panel import SelectionPanel

class SimulatePanel(wx.Panel):
    def __init__(self, publisher, config, **kwargs):
        wx.Panel.__init__(self, **kwargs)
        self.publisher = publisher

        sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.SetSizer(sizer, wx.EXPAND)
        
        sizer.Add(SelectionPanel(parent=self, config=config,
                                 publisher=publisher),
                  proportion=55,
                  flag=config.sizer('basic'),
                  border=config.border('major_section'))

        sizer.Add(ElementsPanel(parent=self, config=config,
                                publisher=publisher,
                                style=config.style('major_section')),
                  proportion=45,
                  flag=config.sizer('basic'),
                  border=config.border('major_section'))
