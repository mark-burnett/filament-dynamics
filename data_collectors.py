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

def record_periodic(f, interval):
    """
    A wrapper function that will calculate 'f' only every 'interval' timesteps.
    """
    def _wrapper(**kwargs):
        if not kwargs['step'] % interval:
            return f(**kwargs)
    return _wrapper

def record_initial(f):
    """
    A wrapper function that will calculate 'f' only for the first timestep.
    """
    def _wrapper(**kwargs):
        if not kwargs['step']:
            return f(**kwargs)
    return _wrapper

def record_final(f, timesteps):
    """
    A wrapper function that will calculate 'f' only for the final timestep.
    """
    t = timesteps - 1
    def _wrapper(**kwargs):
        if not kwargs['step'] == t:
            return f(**kwargs)
    return _wrapper

# Various simple strand measurements.
def strand_growth(**kwargs):
    """
    Returns the how much the strand has grown during the simulation.
    """
    return kwargs['growth']

def strand_length(**kwargs):
    return len(kwargs['strand'])

def count_not(neg_state, **kwargs):
    """
    Counts the number of monomers in the strand not in 'state'.
    """
    s = kwargs['strand']
    return len(s) - s.count(neg_state)

def count(state, **kwargs):
    """
    Counts the number of monomers in the strand in 'state'.
    """
    return kwargs['strand'].count(state)

def tip_state(**kwargs):
    """
    Peeks at the tip state of the strand.
    """
    return kwargs['strand'][-1]
 
# More intensive measurements.
def copy_strand(**kwargs):
    """
    Makes a copy of the entire strand.
    """
    return copy.copy(kwargs['strand'])
