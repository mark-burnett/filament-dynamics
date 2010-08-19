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

class BasicSimulationInfo(wx.Panel):
    def __init__(self, publisher=None, parent=None, config=None, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)

        self.publisher = publisher
        
        self._create_fields(config)
        self._create_sizers(config)

        self.publisher.subscribe(self.update, messages.SimulationInfo)

    def _create_fields(self, config):
        self.simulation_name_text = wx.StaticText(self)
        self.simulation_name_text.SetFont(config.font('item'))

        self.description_text = wx.TextCtrl(self,
                                            style=(wx.TE_MULTILINE |
                                                   wx.TE_READONLY))
        self.description_text.SetFont(config.font('item'))

        self.timestamp_text = wx.StaticText(self)
        self.timestamp_text.SetFont(config.font('item'))

        self.num_par_sets_text = wx.StaticText(self)
        self.num_par_sets_text.SetFont(config.font('item'))

        self.num_runs_text = wx.StaticText(self)
        self.num_runs_text.SetFont(config.font('item'))

    def _create_sizers(self, config):
        outside_sizer = wx.BoxSizer(orient=wx.VERTICAL)

        title_text = wx.StaticText(self, label='Simulation Overview')
        title_text.SetFont(config.font('sub_heading'))

        outside_sizer.Add(title_text,
                          flag=config.sizer('heading'),
                          border=config.border('sub_heading'))
        self.SetSizer(outside_sizer)

        first_row_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        second_row_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        third_row_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        fourth_row_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        fifth_row_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        outside_sizer.Add(first_row_sizer,
                          flag=config.sizer('basic'),
                          border=config.border('item'))
        outside_sizer.Add(second_row_sizer,
                          proportion=1,
                          flag=config.sizer('basic'),
                          border=config.border('item'))
        outside_sizer.Add(third_row_sizer,
                          flag=config.sizer('basic'),
                          border=config.border('item'))
        outside_sizer.Add(fourth_row_sizer,
                          flag=config.sizer('basic'),
                          border=config.border('item'))
        outside_sizer.Add(fifth_row_sizer,
                          flag=config.sizer('basic'),
                          border=config.border('item'))

        # First row
        sim_name_text = wx.StaticText(self, label='Simulation Name:')
        sim_name_text.SetFont(config.font('label'))

        first_row_sizer.Add(sim_name_text,
                            flag=(config.sizer('aligned')|wx.ALIGN_RIGHT),
                            border=config.border('item'))
        first_row_sizer.Add(self.simulation_name_text,
                            proportion=1,
                            flag=(config.sizer('aligned')|wx.ALIGN_LEFT),
                            border=config.border('item'))

        # Second row
        creation_date_text = wx.StaticText(self, label='Creation Date:')
        creation_date_text.SetFont(config.font('label'))

        second_row_sizer.Add(creation_date_text,
                             flag=(config.sizer('aligned')|wx.ALIGN_RIGHT),
                             border=config.border('item'))
        second_row_sizer.Add(self.timestamp_text,
                             proportion=1,
                             flag=(config.sizer('aligned')|wx.ALIGN_LEFT),
                             border=config.border('item'))


        # Third row
        description_label_text = wx.StaticText(self, label='Description:')
        third_row_sizer.Add(description_label_text,
                            flag=(config.sizer('aligned')|wx.ALIGN_RIGHT),
                            border=config.border('item'))

        # Fourth row
        fourth_row_sizer.Add(self.description_text,
                             proportion=1,
                             flag=(config.sizer('aligned')|wx.ALIGN_LEFT),
                             border=config.border('item'))


        # Fifth row
        par_set_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        fifth_row_sizer.Add(par_set_sizer,
                            proportion=1,
                            flag=config.sizer('basic'),
                            border=config.border('item'))

        num_par_set_label = wx.StaticText(self, label='Num Parameter Sets:')
        num_par_set_label.SetFont(config.font('label'))
        par_set_sizer.Add(num_par_set_label,
                          flag=(config.sizer('aligned')|wx.ALIGN_RIGHT),
                          border=config.border('item'))
        par_set_sizer.Add(self.num_par_sets_text,
                          proportion=1,
                          flag=(config.sizer('aligned')|wx.ALIGN_LEFT),
                          border=config.border('item'))

        runs_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        fifth_row_sizer.Add(runs_sizer,
                            proportion=1,
                            flag=config.sizer('basic'),
                            border=config.border('item'))

        num_runs_label = wx.StaticText(self, label='Num Runs:')
        num_runs_label.SetFont(config.font('label'))
        runs_sizer.Add(num_runs_label,
                       flag=(config.sizer('aligned')|wx.ALIGN_RIGHT),
                       border=config.border('item'))
        runs_sizer.Add(self.num_runs_text,
                       proportion=1,
                       flag=(config.sizer('aligned')|wx.ALIGN_LEFT),
                       border=config.border('item'))

    def update(self, message):
        self.simulation_name_text.SetLabel(message.name)
        self.timestamp_text.SetLabel(str(message.timestamp.date()))

        self.description_text.Clear()
        self.description_text.AppendText(message.description)
    
        self.num_par_sets_text.SetLabel(str(message.num_par_sets))
        self.num_runs_text.SetLabel(str(message.num_runs))
