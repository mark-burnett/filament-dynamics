#!/usr/bin/env python
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

import simple
import vectorial

import simulation
import end_conditions

__all__ = ['rates', 'initial_strand', 'depolymerization_simulation']

def rates(parameters, dt, concentrations, barbed_end, pointed_end):
    # Construct barbed end objects.
    if barbed_end:
        # Polymerization
        poly_rates = []
        for species in parameters['barbed_polymerization']:
            c = concentrations[species[1]]
            if c:
                rate = dt * c * species[0]
                poly_rates.append((rate, species[1]))
        bpoly = simple.BarbedPoly(poly_rates)
        poly  = bpoly

        # Depolymerization
        depoly_rates = {}
        for k, v in parameters['barbed_depolymerization'].items():
            if v:
                depoly_rates[k] = dt * v
        bdepoly = simple.BarbedDepoly(depoly_rates)
        depoly  = bdepoly

    # Construct pointed end objects.
    if pointed_end:
        # Polymerization
        poly_rates = []
        for species in parameters['pointed_polymerization']:
            c = concentrations[species[1]]
            if c:
                rate = dt * c * species[0]
                poly_rates.append((rate, species[1]))
        ppoly = simple.PointedPoly(poly_rates)
        poly  = ppoly

        # Depolymerization
        depoly_rates = {}
        for k, v in parameters['pointed_depolymerization'].items():
            if v:
                depoly_rates[k] = dt * v
        pdepoly = simple.PointedDepoly(depoly_rates)
        depoly  = pdepoly

    # Combine if needed
    if barbed_end and pointed_end:
        poly   = simple.Collected_rates(bpoly, ppoly)
        depoly = simple.Collected_rates(bdepoly, pdepoly)

    return poly, depoly

def initial_strand(config, model_type):
    if 'vectorial' == model_type.lower():
        return vectorial.Strand(config['initial_size'],
                                config['initial_state'])
    else:
        raise NotImplementedError("'model_type' = %s is not implemented." % model_type.lower())

def depolymerization_simulation(build_poly, build_depoly,
                                wash_poly, wash_depoly,
                                hydro_rates,
                                poly_dc, depoly_dc, poly_timesteps,
                                depoly_timesteps, model_type):
    if 'vectorial' == model_type.lower():
        poly_sim = simulation.Simulation(build_poly, build_depoly, hydro_rates,
                        poly_dc, end_conditions.Counter(poly_timesteps))
        depoly_sim = simulation.Simulation(wash_poly, wash_depoly, hydro_rates,
                        depoly_dc, end_conditions.Counter(depoly_timesteps))
        return simulation.SimulationSequence([poly_sim, depoly_sim])

    else:
        raise NotImplementedError("'model_type' = %s is not implemented." % model_type.lower())
