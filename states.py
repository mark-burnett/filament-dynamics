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

# Monomer chemical state enumeration
class ChemicalState(object):
    def __init__(self, name):
        self.name = name
    def __eq__(self, sister):
        return self.name == sister.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return "<ChemicalState: %s>" % self

ChemicalState.ATP   = ChemicalState('ATP')
ChemicalState.ADPPi = ChemicalState('ADP-Pi')
ChemicalState.ADP   = ChemicalState('ADP')

# Monomer mechanical state enumeration
class MechanicalState(object):
    def __init__(self, name):
        self.name = name
    def __eq__(self, sister):
        return self.name == sister.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return "<MechanicalState: %s>" % self

MechanicalState.OPEN   = MechanicalState('Open')
MechanicalState.CLOSED = MechanicalState('Closed')
