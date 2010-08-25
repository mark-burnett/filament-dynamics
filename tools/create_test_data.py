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

import argparse
import datetime
import configobj

import elixir

import actin_dynamics.database_model as dbm

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.ini',
                        help='Configuration file name')
    return parser.parse_args()

args = parse_command_line()

dbm.setup_database(configobj.ConfigObj(args.config))

# Create test database

# Hydrolysis States
atp_state = dbm.HydrolysisState(name=u'ATP', description=u'Purely chemical state.')
adppi_state = dbm.HydrolysisState(name=u'ADP-Pi', description=u'Purely chemical state.')
adp_state = dbm.HydrolysisState(name=u'ADP', description=u'Purely chemical state.')

# Parameters (and Parameter Sets)
random_ps = dbm.ParameterSet(name=u'Random')

poly_rate_p = dbm.Parameter(label=dbm.ParameterLabel(
                            name=u'ATP Polymerization Rate'), value=11.6)
depoly_rate_p = dbm.Parameter(label=dbm.ParameterLabel(
                              name=u'ADP Depolymerization Rate'), value=5.4)
cleavage_rate_p = dbm.Parameter(label=dbm.ParameterLabel(
                                name=u'Cleavage Rate'), value=0.3)
release_rate_p = dbm.Parameter(label=dbm.ParameterLabel(
                               name=u'Release Rate'), value=0.003)

atp_conc_p = dbm.Parameter(label=dbm.ParameterLabel(name=u'ATP Concentration'),
                           value=4)

initial_strand_length_p = dbm.Parameter(label=dbm.ParameterLabel(
                                       name=u'Initial Strand Length'),
                                       value=100)

duration_p = dbm.Parameter(label=dbm.ParameterLabel(name=u'Sim duration'),
                           value=30)

random_ps.parameters.append(poly_rate_p)
random_ps.parameters.append(depoly_rate_p)
random_ps.parameters.append(cleavage_rate_p)
random_ps.parameters.append(release_rate_p)
random_ps.parameters.append(atp_conc_p)
random_ps.parameters.append(initial_strand_length_p)
random_ps.parameters.append(duration_p)

psg = dbm.ParameterSetGroup(name=u'Test PSG',
                            description=u'Useless test parameters.')
psg.parameter_sets.append(random_ps)

# Transition Bindings
poly_tb = dbm.Binding(class_name=u'BarbedPolymerization')
poly_tb.parameter_mappings.append(
        dbm.ParameterMapping(parameter_label=poly_rate_p.label,
                             local_name=u'rate'))
poly_tb.state_mappings.append(
        dbm.HydrolysisStateMapping(local_name=u'state',
                                 state=atp_state))

depoly_tb = dbm.Binding(class_name=u'BarbedDepolymerization')
depoly_tb.parameter_mappings.append(
        dbm.ParameterMapping(parameter_label=depoly_rate_p.label,
                             local_name=u'rate'))
depoly_tb.state_mappings.append(
        dbm.HydrolysisStateMapping(local_name=u'state',
                                   state=adp_state))

cleavage_tb = dbm.Binding(class_name=u'RandomHydrolysis')
cleavage_tb.parameter_mappings.append(
        dbm.ParameterMapping(parameter_label=cleavage_rate_p.label,
                             local_name=u'rate'))
cleavage_tb.state_mappings.append(
        dbm.HydrolysisStateMapping(local_name=u'old_state',
                                   state=atp_state))
cleavage_tb.state_mappings.append(
        dbm.HydrolysisStateMapping(local_name=u'new_state',
                                   state=adppi_state))

release_tb = dbm.Binding(class_name=u'RandomHydrolysis')
release_tb.parameter_mappings.append(
        dbm.ParameterMapping(parameter_label=release_rate_p.label,
                             local_name=u'rate'))
release_tb.state_mappings.append(
        dbm.HydrolysisStateMapping(local_name=u'old_state',
                                   state=adppi_state))
release_tb.state_mappings.append(
        dbm.HydrolysisStateMapping(local_name=u'new_state',
                                   state=adp_state))

# Transition Measurement Labels
poly_ml = dbm.MeasurementLabel(name=u'Polymerization Count',
                               description=u'poly measurement description.')
depoly_ml = dbm.MeasurementLabel(name=u'Depolymerization Count',
                                 description=u'depoly measurement description.')
cleavage_ml = dbm.MeasurementLabel(name=u'Cleavage Count',
                                   description=u'cleavage measurement description.')
release_ml = dbm.MeasurementLabel(name=u'Release Count',
                                  description=u'release measurement description.')

# Transitions
poly_t = dbm.Transition(name=u'Polymerization',
                        measurement_label=poly_ml,
                        binding=poly_tb)
depoly_t = dbm.Transition(name=u'Depolymerization',
                          measurement_label=depoly_ml,
                          binding=depoly_tb)
cleavage_t = dbm.Transition(name=u'Cleavage',
                            measurement_label=cleavage_ml,
                            binding=cleavage_tb)
release_t = dbm.Transition(name=u'Release',
                           measurement_label=release_ml,
                           binding=release_tb)


# Explicit Measurements
length_ml = dbm.MeasurementLabel(name=u'Strand Length',
                                 description=u'length measurement description.')
length_binding = dbm.Binding(class_name=u'StrandLength')
length_measurement = dbm.ExplicitMeasurement(measurement_label=length_ml,
                                             binding=length_binding)

# Concentrations
conc_ml = dbm.MeasurementLabel(name=u'ATP Concentration',
                               description=u'Concentration of ATP')
conc_binding = dbm.Binding(class_name=u'FixedConcentration')
conc_binding.parameter_mappings.append(
        dbm.ParameterMapping(parameter_label=atp_conc_p.label,
                             local_name=u'concentration'))
conc = dbm.Concentration(measurement_label=conc_ml,
                         binding=conc_binding,
                         state=atp_state)

# Strand Factory
sf_binding = dbm.Binding(class_name=u'SingleState')
sf_binding.parameter_mappings.append(
        dbm.ParameterMapping(parameter_label=initial_strand_length_p.label,
                             local_name=u'length'))
sf_binding.state_mappings.append(
        dbm.HydrolysisStateMapping(local_name=u'state',
                                   state=adp_state))
strand_factory = dbm.StrandFactory(name=u'Test Strand Factory',
                                   binding=sf_binding)

# End conditions
ec_binding = dbm.Binding(class_name=u'Duration')
ec_binding.parameter_mappings.append(
        dbm.ParameterMapping(parameter_label=duration_p.label,
                             local_name=u'duration'))
ec = dbm.EndCondition(binding=ec_binding)

# Simulations
sim = dbm.Simulation(name=u'Test Simulation.',
                     description=u'Simple simulation to test the DB.',
                     strand_factory=strand_factory,
                     creation_date=datetime.datetime.today())

sim.transitions.append(poly_t)
sim.transitions.append(depoly_t)
sim.transitions.append(cleavage_t)
sim.transitions.append(release_t)

sim.concentrations.append(conc)

sim.explicit_measurements.append(length_measurement)

sim.end_conditions.append(ec)

sim.parameter_set_groups.append(psg)

elixir.session.commit()
