#    Copyright (C) 2011 Mark Burnett
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

import pylab
import numpy

import bisect

from . import measurements
from . import slicing

import actin_dynamics.numerical.measurements
from actin_dynamics import numerical

from actin_dynamics import database
from actin_dynamics.numerical.zero_crossings import zero_crossings

def validate_D(run):
    measurements.line(run.analyses['final_tip_fluctuations'])

def timecourse(run):
    # Plot concentrations
    measurements.line(run.analyses['ATP'], color='red',
            label='[G-ATP-Actin] uM')
#    measurements.line(run.analyses['Pi'], color='green',
#            label='[Pi] uM')
    measurements.line(run.analyses['ADP'], color='blue',
            label='[G-ADP-Actin] uM')
    raw_length = run.analyses['length']
    scaled_length = numerical.measurements.scale(raw_length,
            run.all_parameters['filament_tip_concentration'])
    measurements.line(scaled_length, label='[F-actin]')

    raw_adppi_count = run.analyses['adppi_count']
    scaled_adppi_count = numerical.measurements.scale(raw_adppi_count,
            run.all_parameters['filament_tip_concentration'])
    measurements.line(scaled_adppi_count, label='[F-ADPPi-actin]', color='green')
#    print numpy.array(run.analyses['TAG'])[1]/run.all_parameters['filament_tip_concentration']
#    measurements.line(run.analyses['TAG'], color='cyan', label='NX Events')

    pylab.legend()
    pylab.xlabel('Time (s)')
    pylab.ylabel('Concentration (uM)')

def individual_timecourses(run, xmin=10000, xmax=11000, ymin=2600, ymax=3100):
    pylab.figure()
    pylab.subplot(2,1,1)
    measurements.line(run.analyses['filament_0_length'], color='red')
    measurements.line(run.analyses['filament_1_length'], color='green')
    measurements.line(run.analyses['filament_2_length'], color='blue')
    pylab.xlim(xmin, xmax)
    pylab.ylim(ymin, ymax)

    pylab.subplot(2,1,2)
    measurements.line(run.analyses['filament_0_state'], color='red')
    measurements.line(run.analyses['filament_1_state'], color='green')
    measurements.line(run.analyses['filament_2_state'], color='blue')
    pylab.xlim(xmin, xmax)

def tip_fractions(run, start_time=0):
    single_tip_fraction(run.analyses, index=0, start_time=start_time)
    single_tip_fraction(run.analyses, index=1, start_time=start_time)
    single_tip_fraction(run.analyses, index=2, start_time=start_time)

def single_tip_fraction(analyses, index=0, start_time=0):
    f_state = analyses['filament_%s_state' % index]
    i = bisect.bisect(f_state[0], start_time)
    state_array = numpy.array(f_state[1][i:])
    total = float(len(state_array))
    print 'Filament', index
    print 'ATP Fraction:  ', numpy.sum(state_array == 0) / total
    print 'ADPPi Fraction:', numpy.sum(state_array == 1) / total
    print 'ADP Fraction:  ', numpy.sum(state_array == 2) / total



def D_vs_concentration(session, cc_scale=False, **kwargs):
#    e = session.get_experiment('critical_concentration')
    e = session.get_experiment('fujiwara_2002')
    D_ob = e.objectives['final_diffusion_coefficient']
    D_s = slicing.Slicer.from_objective_bind(D_ob)

    Ds, name, concentration_mesh = D_s.minimum_values('atp_concentration')

    j_ob = e.objectives['final_elongation_rate']
    j_s = slicing.Slicer.from_objective_bind(j_ob)

    js, name, concentration_mesh = j_s.minimum_values('atp_concentration')

    concentration_mesh = concentration_mesh[0]

    if cc_scale:
        cc = zero_crossings(concentration_mesh, js)[0]
        concentration_mesh = numpy.array(concentration_mesh) / cc
        print 'cc =', cc

#    pylab.figure()
    pylab.subplot(2,1,1)
    measurements.line((concentration_mesh, Ds), **kwargs)
    if cc_scale:
        pylab.axvline(x=1, color='black')
    pylab.ylabel('Tip Diffusion Coefficient (mon**2 /s)')

    pylab.subplot(2,1,2)
    zero_concentrations = [concentration_mesh[0], concentration_mesh[-1]]
    zero_values = [0, 0]

    measurements.line((zero_concentrations, zero_values))
    measurements.line((concentration_mesh, js), **kwargs)
    if cc_scale:
        pylab.axvline(x=1, color='black')
    pylab.ylabel('Elongation Rate (mon /s )')

    if cc_scale:
        pylab.xlabel('[G-ATP-actin] (critical concentrations)')
    else:
        pylab.xlabel('[G-ATP-actin] (uM)')
