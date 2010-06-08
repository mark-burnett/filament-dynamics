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

import os
import json

from mako.template import Template

from util.introspection import make_kwargs_ascii

def match_states(iterable1, iterable2):
    s1 = set(iterable1)
    s2 = set(iterable2)
    inter = s1.intersection(s2)
    if inter:
        return '"%s"' % list(inter)[0]
    else:
        raise RuntimeError('No matching states found.')

def get_model_config(parameters, template_name,
                     template_dir, template_extension):
    model_template = Template(filename=os.path.join(template_dir, 'models',
                                  template_name + template_extension))
    return json.loads(model_template.render(**make_kwargs_ascii(parameters)))
    
def get_experiment_config(model_states, parameters, template_name,
                          template_dir, template_extension):
    experiment_template = Template(filename=os.path.join(template_dir,
                                       'experiments',
                                       template_name + template_extension))

    template_parameters = {'model_states': model_states,
                           'match_states': match_states}
    template_parameters.update(parameters['experiment'])

    return json.loads(experiment_template.render(**make_kwargs_ascii(template_parameters)))

def get_stage_configs(model_states, experiment_config, experiment_parameters,
                      template_dir, template_extension):
    stage_configs = []
    for stage_name in experiment_config['stages']:
        stage_template = Template(filename=os.path.join(template_dir,
                            'experiments', 'stages',
                            stage_name + template_extension))
        
        template_parameters = {'model_states': model_states,
                               'match_states': match_states}
        template_parameters.update(experiment_parameters['experiment'])
        template_parameters.update(experiment_parameters['stages'][stage_name])

        stage_configs.append(json.loads(stage_template.render(
            **make_kwargs_ascii(template_parameters))))

    return stage_configs
