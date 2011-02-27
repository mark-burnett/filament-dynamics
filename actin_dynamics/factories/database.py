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

from actin_dynamics import database, primitives

from actin_dynamics import logger

from . import bindings

log = logger.getLogger(__file__)

def make_binds(binds, cls):
    return [cls(label=label, **bind) for label, bind in binds.iteritems()]

def static_model(model_definition):
    m      = database.Model()
    m.name = model_definition.get('name')

    m.transitions    = make_binds(model_definition.get('transitions', {}),
                                  database.TransitionBind)
    m.concentrations = make_binds(model_definition.get('concentrations', {}),
                                  database.ConcentrationBind)
    return m

def static_experiments(experiment_definitions, session_parameters):
    results = []
    log.info('Loading %s experiment definitions.' % len(experiment_definitions))
    for name, expt in experiment_definitions.iteritems():
        log.debug("Loading experiment: '%s'" % name)
        e      = database.Experiment()
        e.name = name

        e.parameters = expt.get('parameters', {})
        log.debug('Found %s parameters.' % len(e.parameters))

        total_parameters = dict(e.parameters)
        total_parameters.update(session_parameters)

        sim = expt.get('simulation', {})

        e.filaments      = make_binds(sim.get('filaments', {}),
                                      database.FilamentBind)
        log.debug('Found %s filament bindings.' % len(e.filaments))

        e.end_conditions = make_binds(sim.get('end_conditions', {}),
                                      database.EndConditionBind)
        log.debug('Found %s end_condition bindings.' % len(e.end_conditions))

        e.measurements   = make_binds(sim.get('measurements', {}),
                                      database.MeasurementBind)
        log.debug('Found %s measurement bindings.' % len(e.measurements))

        e.transitions    = make_binds(sim.get('transitions', {}),
                                      database.TransitionBind)
        log.debug('Found %s transition bindings.' % len(e.transitions))

        e.concentrations = make_binds(sim.get('concentrations', {}),
                                      database.ConcentrationBind)
        log.debug('Found %s concentration bindings.' % len(e.concentrations))

        # analysis configuration
        e.analysis_list = make_binds(expt.get('analyses', {}),
                                     database.AnalysisBind)
        log.debug('Found %s analysis bindings.' % len(e.analysis_list))

        # objective configuration
        obj_defs = expt.get('objectives', {})
        e.objective_list = make_binds(obj_defs.get('executors', {}),
                                      database.ObjectiveBind)
        log.debug('Found %s objective bindings.' % len(e.objective_list))

        load_data(e.objectives, total_parameters, obj_defs.get('loaders', {}))


        results.append(e)

    return results


def load_data(objectives, parameters, definitions):
    '''
    Instantiates file readers.
    Loads data from files.
    Assigns data to objectives.
    '''
    log.debug('Loading data for %s objectives.' % len(definitions))
    file_readers = bindings.dict_multiple(definitions, parameters,
            primitives.file_readers.registry)

    for fr in file_readers:
        log.debug("Loading data for '%s'." % fr.label)
        o = objectives[fr.label]
        o.measurement = fr.run()


def create_static_session(name=None, parameters={}, model={}, experiments={},
                          **kwargs):
    session = database.Session(name=name)
    session.parameters = parameters

    session.models.append(static_model(model))
    session.experiments = static_experiments(experiments, parameters)

    return session
