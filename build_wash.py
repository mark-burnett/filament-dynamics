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

import strand
import sim1d
import data_collectors as dcm

from states import ChemicalState
import compile_dict
import rate_conversions

# Simulation parameters
output_file_name = 'vec_test.pickle'

build_concentration = 6

build_duration  = 60 * 1  # seconds
depoly_duration = 60 * 30 # seconds
dt              = 0.01    # seconds

# Rates
#hydro  = compile_dict.build_lipowsky_coupled(1.0, 3*10**-6, 0.57, 2*10**-6)
hydro  = compile_dict.vectoral(1.0, 0.57)
depoly = { ChemicalState.ATP:   2.2,
           ChemicalState.ADPPi: 0.1,
           ChemicalState.ADP:   2.7 }
poly_rate = 11.6 # per uM per s

# For now we will only sample the depolymerization stage
sample_period  = 20 # seconds
sample_spacing = int(sample_period/dt) # timesteps

# Data collectors
dc = {'length': dcm.record_periodic(dcm.strand_length, sample_spacing)}

# Derived parameters
build_timesteps  = int(build_duration/dt)
depoly_timesteps = int(depoly_duration/dt)

scaled_hydro  = rate_conversions.scale_multiple_rates( hydro, dt )
scaled_depoly = rate_conversions.scale_rates( depoly, dt )
scaled_poly   = dt * poly_rate

# Polymerize the strand
print 'Two step simulation of filament growth/depolymerization.'
print 'Beginning build, concentration:', build_concentration, 'uM',
print 'duration:', build_duration, 's'
the_strand = strand.Strand(100, ChemicalState.ADP)
sim1d.simulate(the_strand, scaled_hydro, scaled_depoly,
               scaled_poly * build_concentration,
               ChemicalState.ATP, build_timesteps, {})
#the_strand._substrands = [(1000, ChemicalState.ADP),
#                          (100,  ChemicalState.ADPPi),
#                          (1000, ChemicalState.ATP)]
print the_strand._substrands

# Depolymerize the strand
print 'Beginning depolymerization, duration:', depoly_duration, 's'
data = sim1d.simulate(the_strand, scaled_hydro, scaled_depoly, 0,
                      ChemicalState.ATP, depoly_timesteps, dc)
print the_strand._substrands

with file(output_file_name, 'wb') as f:
    cPickle.dump({'strand':              the_strand,
                  'data':                data,
                  'build_concentration': build_concentration,
                  'build_duration':      build_duration,
                  'dt':                  dt,
                  'sample_period':       sample_period,
                  'hydro_rates':         hydro,
                  'depoly_rates':        depoly,
                  'poly_rate':           poly_rate},
                  f, True)
