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

from actin_dynamics import database_model as dbm

from . import messages

class GUIHandler(object):
    def __init__(self, publisher):
        self.publisher = publisher

        self._subscribe_to_ui_requests()

    def _subscribe_to_ui_requests(self):
        self.publisher.subscribe(self.simulation_requested,
                                 messages.SimulationRequest)

        self.publisher.subscribe(self.concentration_requested,
                                 messages.ConcentrationRequest)
        self.publisher.subscribe(self.end_condition_requested,
                                 messages.EndConditionRequest)
        self.publisher.subscribe(self.explicit_measurement_requested,
                                 messages.ExplicitMeasurementRequest)
        self.publisher.subscribe(self.parameter_set_requested,
                                 messages.ParameterSetRequest)
        self.publisher.subscribe(self.parameter_set_group_requested,
                                 messages.ParameterSetGroupRequest)
        self.publisher.subscribe(self.strand_factory_requested,
                                 messages.StrandFactoryRequest)
        self.publisher.subscribe(self.transition_requested,
                                 messages.TransitionRequest)

    def initialize(self):
        self.publisher.publish(messages.SimulationList.all())

    def terminate(self):
        pass

    def simulation_requested(self, message):
        '''
            Queries the database for the selected simulation, compiles relevent
        info about the simulation, then publishes the related messages.
        '''
        sim = dbm.Simulation.get(message.id)

        # Provide basic simulation info
        self.publisher.publish(messages.SimulationInfo.from_simulation(sim))

        self.publisher.publish(messages.MeasurementList.from_simulation(sim))
        self.publisher.publish(messages.ParameterSet.from_simulation(sim))

        # Provide top level details of simulation.
        self.publisher.publish(messages.ParameterSetGroupList.from_simulation(sim))

        self.publisher.publish(messages.ConcentrationList.from_simulation(sim))
        self.publisher.publish(messages.EndConditionList.from_simulation(sim))
        self.publisher.publish(messages.ExplicitMeasurementList.from_simulation(sim))
        self.publisher.publish(messages.StrandFactoryList.from_simulation(sim))
        self.publisher.publish(messages.TransitionList.from_simulation(sim))

        # Publish blank TransitionInfo, etc. to clear controls.
#        self.publisher.publish(messages.TransitionInfo())
#        self.publisher.publish(messages.ConcentrationInfo())
#        self.publisher.publish(messages.ExplicitMeasurementInfo())
#        self.publisher.publish(messages.EndConditionInfo())


    def concentration_requested(self, message):
        c = dbm.Concentration.get(message.id)
        self.publisher.publish(messages.ConcentrationInfo.from_concentration(c))

    def end_condition_requested(self, message):
        ec = dbm.EndCondition.get(message.id)
        self.publisher.publish(messages.EndConditionInfo.from_end_condition(ec))

    def explicit_measurement_requested(self, message):
        em = dbm.ExplicitMeasurement.get(message.id)
        self.publisher.publish(messages.ExplicitMeasurementInfo.from_explicit_measurement(em))

    def parameter_set_requested(self, message):
        ps = dbm.ParameterSet.get(message.id)
        self.publisher.publish(messages.ParameterSet.from_parameter_set(ps))

    def parameter_set_group_requested(self, message):
        psg = dbm.ParameterSetGroup.get(message.id)
        self.publisher.publish(messages.ParameterSetList.from_parameter_set_group(psg))

    def strand_factory_requested(self, message):
        sf = dbm.StrandFactory.get(message.id)
        self.publisher.publish(messages.StrandFactoryInfo.from_strand_factory(sf))

    def transition_requested(self, message):
        t = dbm.Transition.get(message.id)
        self.publisher.publish(messages.TransitionInfo.from_transition(t))
