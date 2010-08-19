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

from .menu_bar import MenuBar

from actin_dynamics.presenters import messages

class MainFrame(wx.Frame):
    def __init__(self, publisher, config, *args, **kwargs):
        wx.Frame.__init__(self, parent=None, *args, **kwargs)
        self.publisher = publisher

        self.SetMenuBar(MenuBar(self.publisher, parent_frame=self,
                                config=config))
        self.CreateStatusBar()

        self.Bind(wx.EVT_CLOSE, self._on_exit)

    def _on_exit(self, event):
        self.publisher.publish(messages.ExitProgram('Window Manager event.'))
