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

from . import measurements
from . import slicing

from actin_dynamics.numerical.zero_crossings import zero_crossings


def fluctuation_report(run):
    # Print Summary Values
    print 'D', run.objectives[0].value
    # D (both ways), tip state fractions, average elongation rate
    # effective veloctiy @ tip state

    sample_period = run.all_parameters['sample_period']
    # Plots
    # individual filament lengths, velocities (tip states?)

    # tip state autocorrelations
    pylab.figure()
    measurements.line(run.analyses['atp_autocorrelation'], color='red',
            label='ATP Autocorrelation')
    measurements.line(run.analyses['adppi_autocorrelation'], color='green',
            label='ADPPi Autocorrelation')
    measurements.line(run.analyses['adp_autocorrelation'], color='blue',
            label='ADP Autocorrelation')
    pylab.xlim(0, 5)
    pylab.ylim(-1, 1)
    pylab.legend()

    # threshold velocity autocorrelations
    pylab.figure()
    measurements.line(run.analyses['tau_plus_autocorrelation'], color='blue',
            label='Positive Velocity Autocorrelation')
    measurements.line(run.analyses['tau_minus_autocorrelation'], color='green',
            label='Negative Velocity Autocorrelation')
    pylab.xlim(0, 5)
    pylab.ylim(-1, 1)
    pylab.legend()



def D_vs_concentration(session, cc_scale=False, **kwargs):
    e = session.get_experiment('critical_concentration')
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

    pylab.figure()
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

def elongation_rate_vs_conc(session, **kwargs):
    ob = session.get_experiment('critical_concentration').objectives['final_elongation_rate']

    s = slicing.Slicer.from_objective_bind(ob)

    rs, names, concentration_mesh = s.minimum_values('atp_concentration')

    zero_concentrations = [concentration_mesh[0][0], concentration_mesh[0][-1]]
    zero_values = [0, 0]

    measurements.line((concentration_mesh[0], rs), **kwargs)
    measurements.line((zero_concentrations, zero_values))
    pylab.xlabel('[G-ATP-actin] (uM)')
    pylab.ylabel('Average Elongation Rate (mon / s)')

def get_cc(experiment):
    ob = experiment.objectives['elongation_rate']

    s = slicing.Slicer.from_objective_bind(ob)

    rs, names, concentration_mesh = s.minimum_values('atp_concentration')
    cc = zero_crossings(concentration_mesh[0], rs)[0]

    return cc
