#    Copyright (C) 2009 Mark Burnett
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

class SimpleMeasurement(list):
    __slots__ = ['label']
    def __init__(self, label, *args):
        self.label = label
        list.__init__(self, *args)

    def append(self, time, value):
        list.append(self, (time, value))

    def __str__(self):
        return self.label

class ChangingMeasurement(SimpleMeasurement):
    __slots__ = ['last_value']
    def __init__(self, label, *args):
        self.last_value = None
        SimpleMeasurement.__init__(self, label, *args)

    def append(self, time, value):
        if value != self.last_value:
            self.last_value = value
            SimpleMeasurement.append(self, time, value)
