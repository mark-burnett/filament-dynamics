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

import wx.grid

class _ListTableBase(wx.grid.PyGridTableBase):
    def __init__(self, publisher=None, column_names=None, update_message=None,
                 update_message_field=None,
                 grid=None):
        wx.grid.PyGridTableBase.__init__(self)

        if not column_names:
            raise RuntimeError('"column_names" has zero length.  What a useless list.')
        self.column_names = column_names
        
        if update_message_field is not None:
            self.update_message_field = update_message_field
        else:
            self.update_message_field = 'data'

        self.data = []

        self.grid = grid

        publisher.subscribe(self.update, update_message)

    def GetColLabelValue(self, col):
        return self.column_names[col]

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.column_names)

    def GetValue(self, row, col):
        return self.data[row][col + 1]


    def update(self, message):
        self.direct_update(getattr(message, self.update_message_field))

    def direct_update(self, data):
        self.data = data
        # XXX This SetTable -> ForceRefresh business is a bit of a hack.
        self.grid.SetTable(self)
        self.grid.AutoSizeColumns()
        self.grid.ForceRefresh()

    def get_data(self, row):
        return self.data[row][0]

class UpdatingListCtrl(wx.grid.Grid):
    def __init__(self, publisher, column_names=None, parent=None,
                 update_message=None, selection_message=None,
                 clear_selection_message=None,
                 update_message_field=None,
                 config=None,
                 label_font=None,
                 field_font=None,
                 **kwargs):
        wx.grid.Grid.__init__(self, parent=parent, **kwargs)

        self.table_base = _ListTableBase(publisher=publisher,
                                         column_names=column_names,
                                         update_message=update_message,
                                         update_message_field=update_message_field,
                                         grid=self)

        self.SetTable(self.table_base)

        # Change display options to make it look more like a real list control.
        self.EnableEditing(False)
        self.EnableGridLines(False)

        self.DisableDragRowSize()
        self.DisableDragColSize()

        self.SetSelectionMode(wx.grid.Grid.SelectRows)
        self.SetGridCursor(0, self.GetNumberCols())

        self.AutoSizeColumns()
        self.SetMargins(0, -1)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(wx.grid.GRID_AUTOSIZE)

        # XXX it might be nice to add something like this, but better
#        if selection_message is None:
#            self.Disable()
        
        self.publisher = publisher
        self.selection_message = selection_message
        self.selected_row = None

        if label_font is not None:
            self.SetLabelFont(label_font)
        else:
            self.SetLabelFont(config.font('sub_heading'))

        if field_font is not None:
            self.SetDefaultCellFont(field_font)
        else:
            self.SetDefaultCellFont(config.font('item'))

        if clear_selection_message is not None:
            self.publisher.subscribe(self._clear_selection,
                                     clear_selection_message)

        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self._on_click)

        # events to ignore
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self._ignore_event)

    def _on_click(self, event):
        if self.selection_message is not None:
            row = event.GetRow()
            if row != self.selected_row:
                self.selected_row = row
                self.SelectRow(row)
                self.publisher.publish(self.selection_message(self.table_base.get_data(row)))

    def _ignore_event(self, event):
        pass

    def _clear_selection(self, message):
        self.selected_row = None
        self.ClearSelection()
