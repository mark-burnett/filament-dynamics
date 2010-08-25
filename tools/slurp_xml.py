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
import configobj
import elixir

from lxml import etree

from actin_dynamics import database_model as dbm

def _parse_root(root, class_name):
    results = []
    cls = getattr(dbm, class_name)
    for element in root:
        results.append(cls.from_xml(element))

    return results

def _parse_all_files(class_name, config_filename, filenames):
    dbm.setup_database(configobj.ConfigObj(config_filename))

    xml_parser = etree.XMLParser(dtd_validation=True, load_dtd=True,
                                 remove_comments=True)
    for filename in filenames:
        et = etree.parse(filename, parser=xml_parser)
        results = _parse_root(et.getroot(), class_name)

    elixir.session.commit()


class MeasurementLabelsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        _parse_all_files('MeasurementLabel', namespace.config, values)


class ParameterLabelsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        _parse_all_files('ParameterLabel', namespace.config, values)


class HydrolysisStatesAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        _parse_all_files('HydrolysisState', namespace.config, values)

class ParameterSetGroupsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        _parse_all_files('ParameterSetGroup', namespace.config, values)


class SimulationsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        _parse_all_files('Simulation', namespace.config, values)


def parse_command_line():
    parser = argparse.ArgumentParser()

    command_group = parser.add_mutually_exclusive_group(required=True)
    command_group.add_argument('-ml', '--measurement_labels', nargs='+',
                               action=MeasurementLabelsAction)
    command_group.add_argument('-pl', '--parameter_labels', nargs='+',
                               action=ParameterLabelsAction)
    command_group.add_argument('-hs', '--hydrolysis_states', nargs='+',
                               action=HydrolysisStatesAction)
    command_group.add_argument('-psg', '--parameter_set_groups', nargs='+',
                               action=ParameterSetGroupsAction)
    command_group.add_argument('-s', '--simulations', nargs='+',
                               action=SimulationsAction)

    parser.add_argument('--config', default='config.ini',
                        help='Configuration file name')

    return parser.parse_args()

def main():
    args = parse_command_line()

if '__main__' == __name__:
    main()
