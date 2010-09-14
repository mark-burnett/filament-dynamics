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

class Byproduct(object):
    __slots__ = ['byproduct']
    def __init__(self, byproduct):
        self.byproduct = byproduct

    def perform(self, time, strands, concentrations, index, r):
        concentrations[self.byproduct].add_monomer()

def add_byproduct(old_class):
    '''
    Dynamically create a new transition class that adds byproduct
    functionality.
    '''
    new_class_name = old_class.__name__ + 'WithByproduct'
    new_class_dict = dict(old_class.__dict__)
    new_class_dict['states'].append('byproduct')

    new_class = type(new_class_name, (old_class, Byproduct), new_class_dict)

    def init(self, byproduct=None, **kwargs):
        old_class.__init__(self, **kwargs)
        Byproduct.__init__(self, byproduct=byproduct)

    def perform(self, time, strand, concentrations, index, r):
        old_class.perform(self, time, strand, concentrations, index, r)
        Byproduct.perform(self, time, strand, concentrations, index, r)

    new_class.__init__ = init
    new_class.perform  = perform

    return new_class
