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

class InfoPanel(wx.Panel):
    def __init__(self, publisher=None, parent=None, config=None, **kwargs):
        wx.Panel.__init__(self, parent=parent, **kwargs)
        self.publisher = publisher

        vertical_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.SetSizer(vertical_sizer, wx.EXPAND)

        top_text = wx.StaticText(parent=self, label='Selection Details')
        top_text.SetFont(config.font('sub_heading'))
        vertical_sizer.Add(top_text,
                           flag=(config.sizer('aligned')|wx.ALIGN_CENTER),
                           border=config.border('sub_heading'))

        horizontal_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        vertical_sizer.Add(horizontal_sizer, proportion=1,
                           flag=config.sizer('basic'),
                           border=config.border('item'))
        horizontal_sizer.Add(
                TitledListPanel(publisher=publisher, parent=self, config=config,
                    title='Parameter Mappings',
                    column_names=['Label', 'Local Name'],
                    update_message=view_messages.UpdateParameterMappings,
                    update_message_field='parameter_mappings'),
                             proportion=64, flag=config.sizer('basic'),
                             border=config.border('item'))

        horizontal_sizer.Add(
                TitledListPanel(publisher=publisher, parent=self, config=config,
                    title='State Mappings',
                    column_names=['State', 'Local Name'],
                    update_message=view_messages.UpdateStateMappings,
                    update_message_field='state_mappings'),
                             proportion=36, flag=config.sizer('basic'),
                             border=config.border('item'))

        self._subscribe_to_messages()

    def _subscribe_to_messages(self):
        self.publisher.subscribe(self.concentration_selected,
                                 presenter_messages.ConcentrationInfo)
        self.publisher.subscribe(self.end_condition_selected,
                                 presenter_messages.EndConditionInfo)
        self.publisher.subscribe(self.explicit_measurement_selected,
                                 presenter_messages.ExplicitMeasurementInfo)
        self.publisher.subscribe(self.strand_factory_selected,
                                 presenter_messages.StrandFactoryInfo)
        self.publisher.subscribe(self.transition_selected,
                                 presenter_messages.TransitionInfo)

    def _update_lists(self, message):
        self.publisher.publish(view_messages.UpdateParameterMappings(
            message.parameter_mappings))
        self.publisher.publish(view_messages.UpdateStateMappings(
            message.state_mappings))


    def concentration_selected(self, message):
        # Set top text

        self._update_lists(message)

        # clear other selections
        self.publisher.publish(view_messages.ClearExplicitMeasurementSelection())
        self.publisher.publish(view_messages.ClearEndConditionSelection())
        self.publisher.publish(view_messages.ClearStrandFactorySelection())
        self.publisher.publish(view_messages.ClearTransitionSelection())

    def explicit_measurement_selected(self, message):
        # Set top text

        self._update_lists(message)

        # clear other selections
        self.publisher.publish(view_messages.ClearConcentrationSelection())
        self.publisher.publish(view_messages.ClearEndConditionSelection())
        self.publisher.publish(view_messages.ClearStrandFactorySelection())
        self.publisher.publish(view_messages.ClearTransitionSelection())

    def end_condition_selected(self, message):
        # Set top text

        self._update_lists(message)

        # clear other selections
        self.publisher.publish(view_messages.ClearConcentrationSelection())
        self.publisher.publish(view_messages.ClearExplicitMeasurementSelection())
        self.publisher.publish(view_messages.ClearStrandFactorySelection())
        self.publisher.publish(view_messages.ClearTransitionSelection())

    def strand_factory_selected(self, message):
        # Set top text

        self._update_lists(message)

        # clear other selections
        self.publisher.publish(view_messages.ClearConcentrationSelection())
        self.publisher.publish(view_messages.ClearExplicitMeasurementSelection())
        self.publisher.publish(view_messages.ClearEndConditionSelection())
        self.publisher.publish(view_messages.ClearTransitionSelection())

    def transition_selected(self, message):
        # Set top text

        self._update_lists(message)

        # clear other selections
        self.publisher.publish(view_messages.ClearConcentrationSelection())
        self.publisher.publish(view_messages.ClearExplicitMeasurementSelection())
        self.publisher.publish(view_messages.ClearEndConditionSelection())
        self.publisher.publish(view_messages.ClearStrandFactorySelection())
