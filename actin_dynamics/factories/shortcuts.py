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

import collections

#from bindings import instantiate_binding

#from .. import concentrations
#from .. import end_conditions
#from .. import measurements
#from .. import filaments
#from .. import transitions

def make_filaments(filaments_dict, parameters):
    factory = instantiate_binding(filaments_dict, parameters, filaments.registry)
    return factory.create()

def make_transitions(transitions_dict, parameters):
    return make_from_list(transitions_dict, parameters,
                          transitions.registry)

def make_end_conditions(end_conditions_dict, parameters):
    return make_from_list(end_conditions_dict, parameters,
                          end_conditions.registry)

def make_measurements(measurements_dict, parameters):
    return make_from_list(measurements_dict, parameters, measurements.registry)

def make_from_list(object_dicts, parameters, registry):
    results = []
    for od in object_dicts:
        results.append(instantiate_binding(od, parameters, registry))
    return results

def make_concentrations(concentrations_dict, parameters):
    result = collections.defaultdict(concentrations.ZeroConcentration)
    for conc_dict in concentrations_dict:
        result[conc_dict['state']] = instantiate_binding(
                conc_dict, parameters, concentrations.registry)
    return result
