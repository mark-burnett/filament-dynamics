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

import ppmap

concentrations = [ 0.1 ] #, 0.05, 0.05, 0.05 ]


def sim( c ):
    # FIXME remove seed
    import sys
    sys.path.remove('/usr/share/pyshared')
    import sim1d
    from states import ChemicalState
    import data_collectors
    from numpy.random import mtrand
    mtrand.seed(0)

    duration = 100000
    dt = 0.01
    dc = {'length'   : data_collectors.strand_length,
          'cap_len'  : data_collectors.cap_length,
          'ATP_cap'  : data_collectors.ATP_cap,
          'tip_state': data_collectors.tip_state}

    hydro = { ChemicalState.ATP:   [(0.3,   ChemicalState.ADPPi)],
              ChemicalState.ADPPi: [(0.004, ChemicalState.ADP)],
              ChemicalState.ADP:   [] }
    remove = { ChemicalState.ATP:   1.4,
               ChemicalState.ADPPi: 1.1,
               ChemicalState.ADP:   7.2 }
    addition = 11.6 # per uM per s
    return sim1d.simulate( 10**9, ChemicalState.ADP, hydro, remove,
                           addition * c, ChemicalState.ATP,
                           duration, dt, dc )

outputs = ppmap.ppmap( sim, concentrations )
#outputs = map( sim, concentrations )

def analyze( output ):
    from numpy import average, array
    from states import ChemicalState
    import diffusion

    trash_time = 2500
    dt = 0.01
    trash_samples = int(trash_time/dt)
    length = output['length'   ][ trash_samples: ]
    cl     = output['cap_len'  ][ trash_samples: ]
    ac     = output['ATP_cap'  ][ trash_samples: ]
    ts     = output['tip_state'][ trash_samples: ]
    import cPickle
    cPickle.dump( (length, cl, ac), file('cl.p','wb') )

    D, V, Derr, Verr = diffusion.D_and_V( length, dt )
    cap_len = average(cl)
    atp_len = average(ac)
    tT  = float(sum(array(ts)==ChemicalState.ATP))/len(ts)
    tDp = float(sum(array(ts)==ChemicalState.ADPPi)) /len(ts)
    tD  = float(sum(array(ts)==ChemicalState.ADP))/len(ts)
    return D, V, cap_len, atp_len, tT, tDp, tD

res = ppmap.ppmap( analyze, outputs )

for c, res_tup in zip(concentrations, res):
    D, V, cap_len, atp_len, tT, tDp, tD = res_tup
    print 'Concentration:', c
    print 'D, V:', D, V
    print 'Cap length:', cap_len
    print 'ATP cap length:', atp_len
    print 'Tip ATP fraction:', tT
    print 'Tip ADPPi fraction:', tDp
    print 'Tip ADP fraction:', tD
    print 'Total fraction:', tT + tDp + tD
