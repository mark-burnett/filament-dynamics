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

from bindings import instantiate_binding

from .. import concentrations
from .. import end_conditions
from .. import strand_factories
from .. import transitions
from .. import explicit_measurements

from actin_dynamics.common import logutils
logger = logutils.getLogger(__file__)

__all__ = ['make_concentration', 'make_end_condition', 'make_explicit_measurement',
           'make_strand_factory', 'make_transition']

def make_concentration(parameter_value_map, concentration):
    logger.debug('Making concentration: parameter_value_map=%s, concentration=%s'
                 % (parameter_value_map, concentration))
    c = instantiate_binding(parameter_value_map,
                            concentration.binding,
                            concentrations.registry)
    if concentration.measurement_label:
        c.measurement_label = concentration.measurement_label
    return c

def make_end_condition(parameter_value_map, end_condition):
    logger.debug('Making end condition: parameter_value_map=%s, end_condition=%s'
                 % (parameter_value_map, end_condition))
    return instantiate_binding(parameter_value_map,
                               end_condition.binding,
                               end_conditions.registry)

def make_explicit_measurement(parameter_value_map, explicit_measurement):
    logger.debug('Making explicit measurement: parameter_value_map=%s, explicit_measurement=%s'
                 % (parameter_value_map, explicit_measurement))
    em = instantiate_binding(parameter_value_map, explicit_measurement.binding,
                             explicit_measurements.registry)
    if explicit_measurement.measurement_label:
        em.measurement_label = explicit_measurement.measurement_label
    return em

def make_strand_factory(parameter_value_map, strand_factory_binding):
    logger.debug('Making strand factory: parameter_value_map=%s, strand_factory=%s'
                 % (parameter_value_map, strand_factory))
    return instantiate_binding(parameter_value_map,
                               strand_factory_binding,
                               strand_factories.registry)

def make_transition(parameter_value_map, transition):
    logger.debug('Making transition: parameter_value_map=%s, transition=%s'
                 % (parameter_value_map, transition))
    t = instantiate_binding(parameter_value_map,
                            transition.binding,
                            transitions.registry)
    if transition.measurement_label:
        t.measurement_label = transition.measurement_label
    return t
