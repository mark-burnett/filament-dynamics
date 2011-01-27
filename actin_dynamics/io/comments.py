#    Copyright (C) 2011 Mark Burnett
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

class CommentFilter(object):
    def __init__(self, stream, ownership=False):
        self.stream = stream
        self._ownership = ownership

    @classmethod
    def from_filename(cls, filename):
        return cls(open(filename), ownership=True)

    def __del__(self):
        if self._ownership:
            self.stream.close()

    def __iter__(self):
        return self

    def next(self):
        line = self.stream.next()
        line.strip()
        while line.startswith('#'):
            line = self.stream.next()
            line.strip()

        return line
