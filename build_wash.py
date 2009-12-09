#!/usr/bin/env python
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

import cPickle
from numpy.random import mtrand
from numpy import array

import simulate
import simple_rates
import data_collectors as dcm

from states import ChemicalState

# Simulation parameters
output_file_name = 'allnew_vv.pickle'

build_concentration = 6
poly_rate = 11.6 # per uM per s

build_duration  = 60 * 1  # seconds
depoly_duration = 60 * 60 # seconds
dt              = 0.01    # seconds

# Rates
build_pars  = array([11.6*6, 1.0, 0.57, 2.2, 0.1, 2.7]) * dt
build_rates = simple_rates.vv_from_list(dt * build_pars, ChemicalState.ATP)
postwash_pars  = array([0, 1.0, 0.57, 2.2, 0.1, 2.7]) * dt
postwash_rates = simple_rates.vv_from_list(dt * postwash_pars, None)

# For now we will only sample the depolymerization stage
sample_period  = 20 # seconds

# Derived parameters
build_timesteps  = int(build_duration/dt)
depoly_timesteps = int(depoly_duration/dt)

sample_spacing = int(sample_period/dt) # timesteps

# Data collectors
dc = {'length':         dcm.record_periodic(dcm.strand_length, sample_spacing),
      'initial_strand': dcm.record_initial(dcm.copy_strand),
      'final_strand':   dcm.record_final(dcm.copy_strand, depoly_timesteps)}

# Polymerize the strand
print 'Two step simulation of filament growth/depolymerization.'
print 'Beginning build, concentration:', build_concentration, 'uM',
print 'duration:', build_duration, 's'
the_strand = [ChemicalState.ADP for x in xrange(100)]
simulate.simulate(the_strand, build_timesteps, build_rates, dc, mtrand.rand)

# Depolymerize the strand
print 'Beginning depolymerization, duration:', depoly_duration, 's'
data = simulate.simulate(the_strand, build_timesteps, postwash_rates, dc,
                       mtrand.rand)

with file(output_file_name, 'wb') as f:
    cPickle.dump({'data':                data,
                  'build_concentration': build_concentration,
                  'build_duration':      build_duration,
                  'dt':                  dt,
                  'sample_period':       sample_period},
                  f, True)
