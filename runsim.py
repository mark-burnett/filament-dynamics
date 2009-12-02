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
from multiprocessing import Pool, Process

import strand
import sim1d
import data_collectors as dcm

from states import ChemicalState
import compile_dict
import rate_conversions

# Simulation parameters
output_file_name = '0_1_10000s_1run.pickle'

concentrations = [0.1]

duration = 10000
dt       = 0.01 # seconds

sample_period = 10 # seconds
sample_spacing = int(sample_period/dt) # timesteps

possible_states = [ChemicalState.ATP, ChemicalState.ADPPi, ChemicalState.ADP]
base_hydro = [ [(0.3, ChemicalState.ADPPi)], [(0.004, ChemicalState.ADP)], [] ]
hydro = compile_dict.uncoupled(possible_states, base_hydro)

depoly = { ChemicalState.ATP:   1.4,
           ChemicalState.ADPPi: 1.1,
           ChemicalState.ADP:   7.2 }
poly_rate = 11.6 # per uM per s

dc = {'length'   : dcm.record_periodic(dcm.strand_length, sample_spacing),
      'cap_len'  : dcm.record_periodic(
          lambda **a: dcm.count_not(ChemicalState.ADP,**a), sample_spacing),
      'ATP_cap'  : dcm.record_periodic(
          lambda **a: dcm.count(ChemicalState.ATP, **a), sample_spacing),
      'tip_state': dcm.record_periodic(dcm.tip_state, sample_spacing)}

# Derived parameters
timesteps = int(duration/dt)

scaled_hydro  = rate_conversions.scale_multiple_rates( hydro, dt )
scaled_depoly = rate_conversions.scale_rates( depoly, dt )
scaled_poly   = dt * poly_rate

# This cannot be a lambda expression.  You have to write it out explicitly
# to avoid a pickling error.
def sim(c):
    the_strand = strand.Strand(10**9, ChemicalState.ADP)
    data = sim1d.simulate(the_strand,
                          scaled_hydro, scaled_depoly, scaled_poly * c,
                          ChemicalState.ATP, timesteps, dc)
    return (the_strand, data)

if '__main__' == __name__:
    p = Pool()
    try:
        outputs = p.map(sim, concentrations)
        p.close()
        p.join()
    except KeyboardInterrupt:
        p.terminate()
    with file(output_file_name, 'wb') as f:
        cPickle.dump({'concentrations': concentrations, 'data': outputs,
                      'duration': duration, 'dt': dt,
                      'sample_period': sample_period,
                      'hydro_rates': hydro, 'depoly_rates': depoly,
                      'poly_rate': poly_rate},
                      f, True)
