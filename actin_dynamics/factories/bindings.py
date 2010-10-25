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

def instantiate_binding(object_dict, parameters, registry):
    cls = registry[object_dict['class_name']]
    par_map = object_dict['parameters']
    kwargs = dict((local_name, parameters[global_name])
                  for local_name, global_name in par_map.iteritems())
    # NOTE getattr doesn't appear to work on yaml 'dicts' for some reason.
    try:
        fixed_pars = object_dict['fixed_parameters']
        kwargs.update(fixed_pars)
    except:
        pass

    return cls(**kwargs)
