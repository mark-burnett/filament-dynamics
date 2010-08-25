#!/usr/bin/env bash

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

echo 'Dropping old database.'
sudo -u postgres dropdb actin_dynamics

echo 'Creating new database.'
sudo -u postgres createdb -O aduser actin_dynamics

echo 'Creating tables.'
python tools/create_tables.py

echo 'Creating test data.'
#python tools/create_test_data.py
python tools/slurp_xml.py --measurement_labels data/xml/measurement_labels.xml
python tools/slurp_xml.py --parameter_labels data/xml/parameter_labels.xml
python tools/slurp_xml.py --hydrolysis_states data/xml/hydrolysis_states.xml

python tools/slurp_xml.py --simulations data/xml/simulations/*.xml
