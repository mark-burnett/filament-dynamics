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

import rates
import models

import data_collectors
import end_conditions
import simulation

def build_depolymerization_simulation(model_type, parameters,
                                      dt, measurement_period,
                                      polymerization_timesteps,
                                      depolymerization_timesteps,
                                      polymerization_concentrations,
                                      barbed_end=True, pointed_end=False):
    # Adjust raw on/off parameters by dt.
    if barbed_end:
        barbed_poly_rates   = rates.polymerization.time_adjust(dt,
                config['parameters']['barbed_polymerization'])
        barbed_depoly_rates = rates.depolymerization.time_adjust(dt,
                config['parameters']['barbed_depolymerization'])
    else:
        barbed_poly_rates   = None
        barbed_depoly_rates = None

    if pointed_end:
        pointed_poly_rates   = rates.polymerization.time_adjust(dt,
                config['parameters']['pointed_polymerization'])
        pointed_depoly_rates = rates.depolymerization.time_adjust(dt,
                config['parameters']['pointed_depolymerization'])
    else:
        pointed_poly_rates   = None
        pointed_depoly_rates = None
    
    hydrolysis_rates = rates.hydrolysis.time_adjust(dt,
            config['parameters']['hydrolysis_rates'])

    # Convert rates to model objects.
    poly   = rates.polymerization.fixed_concentration(barbed_poly_rates,
                    pointed_poly_rates, polymerization_concentrations)
    depoly = rates.depolymerization.independent(barbed_depoly_rates,
                                                pointed_depoly_rates)
    hydro  = models.hydrolysis[model_type](hydrolysis_rates)

    # Construct data collectors.
    dcs = {'length':data_collectors.RecordPeriodic(
                    data_collectors.strand_length, measurement_period)}

    # Construct simulation.
    return simulation.SimulationSequence([
        simulation.Simulation(poly, depoly, hydro, {},
            end_conditions.RandomCounter(polymerization_timesteps)),
        simulation.Simulation(rates.NoOp(), depoly, hydro, dcs,
            end_conditions.Counter(depolymerization_timesteps))])
