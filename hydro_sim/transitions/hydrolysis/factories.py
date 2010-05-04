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

import predicates
from implementation import Hydrolysis

def Random(concentrations, old_state, rate, new_state):
    return Hydrolysis(predicates.Random(old_state), rate, new_state)

def Cooperative(concentrations, old_state, pointed_neighbor, rate, new_state):
    return Hydrolysis(predicates.Cooperative(old_state, pointed_neighbor),
                      rate, new_state)
