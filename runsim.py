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
import data_collectors
from states import ChemicalState
import rate_conversions

# Simulation parameters
output_file_name='0_15_10,000s.pickle'
concentrations = [0.15] #[ 0.01, 0.02, 0.03, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1 ]
duration   = 10000
dt = 0.01

hydro  = { ChemicalState.ATP:   [(0.3,   ChemicalState.ADPPi)],
           ChemicalState.ADPPi: [(0.004, ChemicalState.ADP)],
           ChemicalState.ADP:   [] }
depoly = { ChemicalState.ATP:   1.4,
           ChemicalState.ADPPi: 1.1,
           ChemicalState.ADP:   7.2 }
poly_rate = 11.6 # per uM per s

dc = {'length'   : data_collectors.strand_length,
      'cap_len'  : lambda **a: data_collectors.count_not(ChemicalState.ADP,**a),
      'ATP_cap'  : lambda **a: data_collectors.count(ChemicalState.ATP, **a),
      'tip_state': data_collectors.tip_state}

# Derived parameters
timesteps = int(duration/dt)

scaled_hydro  = rate_conversions.scale_multiple_rates( hydro, dt )
scaled_depoly = rate_conversions.scale_rates( depoly, dt )
scaled_poly   = dt * poly_rate

# This cannot be a lambda expression.  You have to write it out explicitly
# to avoid a pickling error.
def sim(c):
    return sim1d.simulate(strand.Strand(10**9, ChemicalState.ADP), 
                          scaled_hydro, scaled_depoly, scaled_poly * c,
                          ChemicalState.ATP, timesteps, dc)

if '__main__' == __name__:
    p = Pool()
    try:
        outputs = p.map(sim, concentrations)
        p.close()
        p.join()
    except KeyboardInterrupt:
        p.terminate()
    cPickle.dump({'concentrations': concentrations, 'data': outputs,
                  'duration': duration, 'dt': dt,
                  'hydro_rates': hydro, 'depoly_rates': depoly,
                  'poly_rate': poly_rate},
                 file(output_file_name,'wb'), True)
