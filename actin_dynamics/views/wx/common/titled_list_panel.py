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
from updating_list_ctrl import UpdatingListCtrl

class TitledListPanel(wx.Panel):
    def __init__(self, title='', font=None, parent=None, publisher=None,
                 config=None, column_names=None, update_message=None,
                 update_message_field=None, selection_message=None,
                 clear_selection_message=None, title_font=None,
                 **kwargs):
        wx.Panel.__init__(self, parent=parent, **kwargs)

        sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.SetSizer(sizer, wx.EXPAND)

        text = wx.StaticText(self, label=title)
        if title_font is not None:
            text.SetFont(title_font)
        else:
            text.SetFont(config.font('sub_heading'))

        sizer.Add(text, flag=config.sizer('heading'),
                  border=config.border('sub_heading'))

        sizer.Add(UpdatingListCtrl(parent=self,
                                   publisher=publisher,
                                   column_names=column_names,
                                   update_message=update_message,
                                   update_message_field=update_message_field,
                                   selection_message=selection_message,
                                   clear_selection_message=clear_selection_message,
                                   config=config,
                                   style=wx.SUNKEN_BORDER),
                  proportion=1,
                  flag=config.sizer('basic'),
                  border=config.border('item'))

