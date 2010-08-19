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

from actin_dynamics.presenters import messages

class RunSimulationPanel(wx.Panel):
    def __init__(self, publisher=None, parent=None, config=None, **kwargs):
        wx.Panel.__init__(self, parent=parent, **kwargs)

        self._create_controls(config)
        self._create_layout(config)

        self.publisher = publisher

    def _create_controls(self, config):
        # XXX Consider Combo box instead?
        self.psg_text = wx.TextCtrl(parent=self)
        self.psg_text.SetFont(config.font('item'))

        self.ps_text = wx.TextCtrl(parent=self)
        self.ps_text.SetFont(config.font('item'))

        self.num_text = wx.TextCtrl(parent=self)
        self.num_text.SetFont(config.font('item'))

        self.run_button = wx.Button(parent=self, label='Run')
        self.run_button.SetFont(config.font('sub_heading'))

    def _create_layout(self, config):
        outer_vertical_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.SetSizer(outer_vertical_sizer, wx.EXPAND)

        title_text = wx.StaticText(parent=self, label='Run Simulation')
        title_text.SetFont(config.font('sub_heading'))

        outer_vertical_sizer.Add(title_text, flag=config.sizer('heading'),
                                 border=config.border('sub_heading'))

        psg_label = wx.StaticText(parent=self, label='Parameter Set Group:')
        psg_label.SetFont(config.font('label'))
        outer_vertical_sizer.Add(psg_label,
                                 flag=config.sizer('basic'),
                                 border=config.border('item'))
        outer_vertical_sizer.Add(self.psg_text,
                                 flag=config.sizer('basic'),
                                 border=config.border('item'))

        ps_label_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        outer_vertical_sizer.Add(ps_label_sizer, flag=config.sizer('basic'),
                                 border=config.border('item'))

        ps_label = wx.StaticText(parent=self, label='Parameter Set:')
        ps_label_sizer.Add(ps_label,
                           proportion=6,
                           flag=(config.sizer('aligned')|wx.ALIGN_LEFT),
                           border=config.border('item'))

        all_label = wx.StaticText(parent=self, label='All')
        all_label.SetFont(config.font('label'))
        ps_label_sizer.Add(all_label,
                           proportion=1,
                           flag=(config.sizer('aligned')|wx.ALIGN_RIGHT),
                           border=config.border('item'))

        ps_ctrl_row_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        outer_vertical_sizer.Add(ps_ctrl_row_sizer, flag=config.sizer('basic'),
                                 border=config.border('item'))

        ps_ctrl_row_sizer.Add(self.ps_text, proportion=1,
                             flag=config.sizer('basic'),
                             border=config.border('item'))

        ps_ctrl_row_sizer.Add(wx.CheckBox(parent=self),
                              flag=config.sizer('basic'),
                              border=config.border('item'))

        # XXX add num runs of this par set/group so far?
        go_row_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        outer_vertical_sizer.Add(go_row_sizer, flag=config.sizer('basic'),
                                 border=config.border('item'))

        num_label = wx.StaticText(parent=self, label='Number:')
        num_label.SetFont(config.font('label'))
        go_row_sizer.Add(num_label, flag=config.sizer('basic'),
                         border=config.border('item'))
        go_row_sizer.Add(self.num_text,
                         proportion=1,
                         flag=config.sizer('basic'),
                         border=config.border('item'))

        outer_vertical_sizer.Add(self.run_button, flag=config.sizer('basic'),
                                 border=config.border('item'))
