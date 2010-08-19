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

from ..common.titled_list_panel import TitledListPanel

from actin_dynamics.presenters import messages

class ParametersPanel(wx.Panel):
    def __init__(self, publisher=None, parent=None, config=None, **kwargs):
        wx.Panel.__init__(self, parent=parent, **kwargs)

        sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.SetSizer(sizer, wx.EXPAND)

        vertical_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        sizer.Add(vertical_sizer, proportion=45, flag=config.sizer('basic'),
                  border=config.border('item'))

        ps_title= wx.StaticText(parent=self, label='Parameter Sets')
        ps_title.SetFont(config.font('sub_heading'))
        vertical_sizer.Add(ps_title, flag=config.sizer('heading'),
                           border=config.border('sub_heading'))

        # XXX style
        vertical_sizer.Add(ParameterSetGroupTree(parent=self, config=config,
                                                 style=(wx.SUNKEN_BORDER |
                                                        wx.TR_DEFAULT_STYLE |
                                                        wx.TR_HIDE_ROOT),
                                                 publisher=publisher),
                           proportion=1, flag=config.sizer('basic'),
                           border=config.border('item'))

        sizer.Add(TitledListPanel(title='Simulation Parameters', parent=self,
                                  publisher=publisher, config=config,
                                  column_names=['Name', 'Value'],
                                  update_message=messages.ParameterSet),
                  proportion=55, flag=config.sizer('basic'),
                  border=config.border('item'))

class ParameterSetGroupTree(wx.TreeCtrl):
    def __init__(self, parent=None, publisher=None, config=None, **kwargs):
        wx.TreeCtrl.__init__(self, parent=parent, **kwargs)

        self.publisher = publisher

        self.last_expanded_group = None
        self._create_root()

        self.SetFont(config.font('item'))

        self.publisher.subscribe(self.update_groups, messages.ParameterSetGroupList)
        self.publisher.subscribe(self.update_sets, messages.ParameterSetList)

        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self._on_expand)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self._on_select_changed)

    def update_groups(self, message):
        self.CollapseAndReset(self.root)
        self.Expand(self.root)
        for id, name in message.parameter_set_groups:
            child = self.AppendItem(self.root, name)
            self.SetPyData(child, id)
            self.SetItemHasChildren(child)

    def update_sets(self, message):
        self.DeleteChildren(self.last_expanded_group)
        for id, name in message.parameter_sets:
            if name:
                child = self.AppendItem(self.last_expanded_group, name)
            else:
                child = self.AppendItem(self.last_expanded_group, str(id))
            self.SetPyData(child, id)

    def _create_root(self):
        self.root = self.AddRoot('Parameter Sets')
        self.SetItemHasChildren(self.root)
        self.Expand(self.root)

    def _on_expand(self, event):
        if event.GetItem() != self.root:
            self.last_expanded_group = event.GetItem()
            self.publisher.publish(messages.ParameterSetGroupRequest(
                self.GetPyData(self.last_expanded_group)))

    def _on_select_changed(self, event):
        item = event.GetItem()
        if not self.ItemHasChildren(item):
            self.publisher.publish(messages.ParameterSetRequest(
                self.GetPyData(item)))
        else:
            self.Expand(item)
