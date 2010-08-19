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

from ..common.titled_list_panel import TitledListPanel
from .basic_sim_info_panel import BasicSimulationInfo
from .parameters_panel import ParametersPanel
from .run_simulation_panel import RunSimulationPanel

class SelectionPanel(wx.Panel):
    def __init__(self, publisher=None, parent=None, config=None, **kwargs):
        wx.Panel.__init__(self, parent=parent, **kwargs)

        outer_vertical_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.SetSizer(outer_vertical_sizer, wx.EXPAND)

        first_row_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        second_row_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        outer_vertical_sizer.Add(first_row_sizer, proportion=1,
                                 flag=config.sizer('basic'),
                                 border=config.border('item'))
        outer_vertical_sizer.Add(second_row_sizer, #proportion=1,
                                 flag=config.sizer('basic'),
                                 border=config.border('item'))

        first_row_sizer.Add(
                TitledListPanel(title='Simulations', parent=self,
                                publisher=publisher, config=config,
                                column_names=['Name', 'Description'],
                                update_message=messages.SimulationList,
                                selection_message=messages.SimulationRequest),
                            proportion=65,
                            flag=config.sizer('basic'),
                            border=config.border('item'))
        first_row_sizer.Add(
                TitledListPanel(title='Measurements', parent=self,
                                publisher=publisher, config=config,
                                column_names=['Name'],
                                update_message=messages.MeasurementList),
                            proportion=35,
                            flag=config.sizer('basic'),
                            border=config.border('item'))

        # XXX Should this be border('item') or border('minor_section')?
        second_row_sizer.Add(BasicSimulationInfo(publisher, parent=self,
                                                 config=config),
                             proportion=60, flag=config.sizer('basic'),
                             border=config.border('minor_section'))
        second_row_sizer.Add(RunSimulationPanel(publisher=publisher, parent=self,
                                                config=config),
                             proportion=40, flag=config.sizer('basic'),
                             border=config.border('item'))

        # XXX Should this be border('item') or border('minor_section')?
        outer_vertical_sizer.Add(ParametersPanel(parent=self,
                                                 publisher=publisher,
                                                 config=config),
                                 proportion=1, flag=config.sizer('basic'),
                                 border=config.border('minor_section'))
