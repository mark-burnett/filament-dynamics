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

from states import ChemicalState

def strand_length( strand, added, removed, i ):
    return added - removed

def cap_length( strand, added, removed, i ):
    return strand.count_not(ChemicalState.ADP)

def ATP_cap( strand, added, removed, i ):
    return strand.count(ChemicalState.ATP)

def tip_state( strand, added, removed, i ):
    return strand.peek()
