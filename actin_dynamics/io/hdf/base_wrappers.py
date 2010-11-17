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

class Wrapper(object):
    def __init__(self, pytables_object=None):
        self._pytables_object = pytables_object

    def __str__(self):
        return str(self._pytables_object)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self._pytables_object))

    @property
    def name(self):
        return self._pytables_object._v_name

#    def __getattr__(self, name):
#        result = getattr(self._pytables_object, '_v_%s' % name, None)
#        if result is not None:
#            return result
#        raise AttributeError('%s not found in %s.'
#                             % (name, self.__class__.__name__))
