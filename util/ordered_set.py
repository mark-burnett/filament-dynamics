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

class OrderedSet(object):
    __slots__ = ['_list', '_dict']
    def __init__(self, iterable=None):
        if iterable:
            self._list = list(iterable)
        else:
            self._list = []
        self._dict = dict((v, i) for i, v in enumerate(self._list))

    def add(self, item):
        if item not in self._dict:
            self._dict[item] = len(self._list)
            try:
                self._list.append(item)
            finally:
                self._dict.pop(item)

    def remove(self, item):
        i = self._dict.pop(item)
        del self._list[i]

    def discard(self, item):
        try:
            i = self._dict.pop(item)
            del self._list[i]
        except KeyError:
            pass

    def __getitem__(self, index):
        return self._list[index]

    def __len__(self):
        return len(self._dict)

    def __contains__(self, item):
        return item in self._dict
