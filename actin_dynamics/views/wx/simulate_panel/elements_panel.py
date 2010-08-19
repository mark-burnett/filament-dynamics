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

from actin_dynamics.presenters import messages as presenter_messages
from .. import messages as view_messages

from ..common.titled_list_panel import TitledListPanel

from .info_panel import InfoPanel

class ElementsPanel(wx.Panel):
    def __init__(self, publisher=None, parent=None, config=None, **kwargs):
        wx.Panel.__init__(self, parent=parent, **kwargs)

        outer_vertical_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.SetSizer(outer_vertical_sizer, wx.EXPAND)

        outer_vertical_sizer.Add(
                TitledListPanel(title='Transitions', parent=self,
                                publisher=publisher, config=config,
                                column_names=['Name', 'Class Name',
                                              'Measurement Label'],
                                update_message=presenter_messages.TransitionList,
                                selection_message=presenter_messages.TransitionRequest,
                                clear_selection_message=view_messages.ClearTransitionSelection),
                             proportion=35, flag=config.sizer('basic'),
                             border=config.border('item'))

        outer_vertical_sizer.Add(
                TitledListPanel(title='Concentrations', parent=self,
                                publisher=publisher, config=config,
                                column_names=['State', 'Class Name',
                                              'Measurement Label'],
                                update_message=presenter_messages.ConcentrationList,
                                selection_message=presenter_messages.ConcentrationRequest,
                                clear_selection_message=view_messages.ClearConcentrationSelection),
                            proportion=20, flag=config.sizer('basic'),
                            border=config.border('item'))

        inner_horizontal_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        outer_vertical_sizer.Add(inner_horizontal_sizer, proportion=20,
                                 flag=config.sizer('basic'),
                                 border=config.border('item'))

        inner_horizontal_sizer.Add(
                TitledListPanel(title='Explicit Measurements', parent=self,
                                publisher=publisher, config=config,
                                column_names=['Label',
                                              'Class Name'],
                                update_message=presenter_messages.ExplicitMeasurementList,
                                selection_message=presenter_messages.ExplicitMeasurementRequest,
                                clear_selection_message=view_messages.ClearExplicitMeasurementSelection),
                            proportion=50, flag=config.sizer('basic'),
                            border=config.border('item'))

        inner_horizontal_sizer.Add(
                TitledListPanel(title='End Conditions', parent=self,
                                publisher=publisher, config=config,
                                column_names=['Class Name'],
                                update_message=presenter_messages.EndConditionList,
                                selection_message=presenter_messages.EndConditionRequest,
                                clear_selection_message=view_messages.ClearEndConditionSelection),
                            proportion=25, flag=config.sizer('basic'),
                            border=config.border('item'))

        inner_horizontal_sizer.Add(
                TitledListPanel(title='Strand Factory', parent=self,
                                publisher=publisher, config=config,
                                column_names=['Class Name'],
                                update_message=presenter_messages.StrandFactoryList,
                                selection_message=presenter_messages.StrandFactoryRequest,
                                clear_selection_message=view_messages.ClearStrandFactorySelection),
                            proportion=25, flag=config.sizer('basic'),
                            border=config.border('item'))

        outer_vertical_sizer.Add(wx.StaticLine(parent=self),
                                 flag=config.sizer('basic'),
                                 border=config.border('item'))
                                 

        outer_vertical_sizer.Add(InfoPanel(parent=self, config=config,
                                           publisher=publisher,
                                           style=config.style('minor_section')),
                                 proportion=25, flag=config.sizer('basic'),
                                 border=config.border('item'))
