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

from actin_dynamics import database

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

def static_experiments(experiment_definitions):
    results = []
    for name, expt in experiment_definitions.iteritems():
        e      = database.Experiment()
        e.name = name
        e.parameters = expt.get('parameters', {})

        e.filaments      = make_binds(expt.get('filaments', {}),
                                      database.FilamentBind)
        e.end_conditions = make_binds(expt.get('end_conditions', {}),
                                      database.EndConditionBind)
        e.measurements   = make_binds(expt.get('measurements', {}),
                                      database.MeasurementBind)
        e.transitions    = make_binds(expt.get('transitions', {}),
                                      database.TransitionBind)
        e.concentrations = make_binds(expt.get('concentrations', {}),
                                      database.ConcentrationBind)

        # analysis configuration
        e.analysis = make_binds(expt.get('analyses', {}), database.AnalysisBind)

        # objective configuration
        obj_defs = expt.get('objectives', {})
        e.objective = make_binds(obj_defs.get('executors', {}),
                                 database.ObjectiveBind)
        e.data = load_data(expt.get(obj_defs.get('loaders', {})))


        results.append(e)

    return results


def load_data(definition):
    loader_binds = make_binds(definition, database.FileReaders)
    loaders = factories.bindings.db_multiple(loader_binds, {})
    return [l.run() for l in loaders]


def create_static_session(name=None, parameters={}, model={}, experiments={},
                          **kwargs):
    session = database.Session(name=name)
    session.parameters = parameters

    session.models.append(static_model(model))
    session.experiments = static_experiments(experiments)

    return session

