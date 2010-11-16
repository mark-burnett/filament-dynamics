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

class GroupWrapper(object):
    def __init__(self, group=None):
        self.group = group

    def __str__(self):
        return str(self.group)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.group))

    @classmethod
    def create(cls, parent_group=None, name=None):
        hdf_file = parent_group._v_file
        group = hdf_file.createGroup(parent_group, name)
        return cls(group)

    def create_subgroup(self, name=None, description=None,
                        wrapper=None):
        if wrapper is None:
            wrapper = self.__class__
        hdf_file = self.group._v_file
        subgroup = hdf_file.create_subgroup(self.group, name, description)
        return wrapper(subgroup)

    def create_table(self, name=None, wrapper=None):
        return wrapper.create(parent_group=self.group, name=name)


class Collection(GroupWrapper):
    def __iter__(self):
        return _WrappedIterator(self.group, self.child_wrapper)

    def create_child(self, name=None):
        return self.child_wrapper.create(parent_group=self.group, name=name)

    def write(self, children):
        for name, data in children.iteritems():
            c = self.child_wrapper.create(parent_group=self.group, name=name)
            c.write(data)


class _WrappedIterator(object):
    def __init__(self, target, wrapper):
        self.target = iter(target)
        self.wrapper = wrapper

    def __iter__(self):
        return self

    def next(self):
        return self.wrapper(next(self.target))
