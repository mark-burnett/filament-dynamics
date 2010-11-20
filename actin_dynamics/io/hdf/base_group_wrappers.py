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

from . import base_wrappers as _base_wrappers

class GroupWrapper(_base_wrappers.Wrapper):
    def __init__(self, group=None):
        _base_wrappers.Wrapper.__init__(self, group)

    @classmethod
    def create(cls, parent_group=None, name=None):
        hdf_file = parent_group._v_file
        group = hdf_file.createGroup(parent_group, name)
        return cls(group)

    @classmethod
    def create_or_select(cls, parent_group=None, name=None):
        try:
            return cls.create(parent_group=parent_group, name=name)
        except:
            return cls(getattr(parent_group, name))


    def create_subgroup(self, name=None, description=None,
                        wrapper=None):
        if wrapper is None:
            wrapper = self.__class__
        hdf_file = self._pytables_object._v_file
        subgroup = hdf_file.createGroup(self._pytables_object, name,
                                        description)
        return wrapper(subgroup)

    def create_table(self, name=None, wrapper=None):
        return wrapper.create(parent_group=self._pytables_object, name=name)

    def delete_children(self):
        for child in self._pytables_object._v_children.values():
            child._f_remove(recursive=True)


class Collection(GroupWrapper):
    def __iter__(self):
        return _WrappedIterator(self._pytables_object, self.child_wrapper)

    def create_child(self, name=None):
        foo = self.child_wrapper.create(parent_group=self._pytables_object,
                                         name=name)
        return foo

    def create_or_select_child(self, name=None):
        child_pytables_object = getattr(self._pytables_object, name, None)
        if child_pytables_object is not None:
            return self.child_wrapper(child_pytables_object)
        else:
            return self.create_child(name=name)

    def write(self, children):
        for name, data in children.iteritems():
            c = self.child_wrapper.create(parent_group=self._pytables_object,
                                          name=name)
            c.write(data)

    def __len__(self):
        return self._pytables_object._v_nchildren

    def __getattr__(self, key):
        return self.child_wrapper(getattr(self._pytables_object, key))


class _WrappedIterator(object):
    def __init__(self, target, wrapper):
        self.target = iter(target)
        self.wrapper = wrapper

    def __iter__(self):
        return self

    def next(self):
        return self.wrapper(next(self.target))
