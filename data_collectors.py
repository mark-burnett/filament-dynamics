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

import copy

def record_periodic(f, interval, **kwargs):
    """
    A wrapper function that will calculate 'f' only every 'interval' timesteps.
    """
    if not kwargs['iteration'] % interval:
        return f(**kwargs)

# Various simple strand measurements.
def strand_length(**kwargs):
    """
    Returns the length of the strand.
    """
    return kwargs['length']

def explicit_strand_length(**kwargs):
    """
    A slower alternative for 'strand_length'.
    """
    return len(kwargs['strand'])

def count_not(neg_state, **kwargs):
    """
    Counts the number of monomers in the strand not in 'state'.
    """
    return kwargs['strand'].count_not(neg_state)

def count(state, **kwargs):
    """
    Counts the number of monomers in the strand in 'state'.
    """
    return kwargs['strand'].count(state)

def tip_state(**kwargs):
    """
    Peeks at the tip state of the strand.
    """
    return kwargs['strand'].peek()
 
# More intensive measurements.
def copy_strand(**kwargs):
    """
    Makes a copy of the entire strand.
    """
    return copy.copy(kwargs['strand'])
