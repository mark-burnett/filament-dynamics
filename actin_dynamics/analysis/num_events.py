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

def get_num_events(parameter_set):
    num_events = 0
    for simulation in parameter_set['simulations']:
        for filament in simulation['filaments']:
            m = filament['measurements']
            num_events += len(m['barbed_pyrene_atp_polymerization'][0]) - 1
            num_events += len(m['barbed_pyrene_adppi_polymerization'][0]) - 1
            num_events += len(m['barbed_pyrene_adp_polymerization'][0]) - 1
            num_events += len(m['barbed_adp_polymerization'][0]) - 1

            num_events += len(m['pointed_pyrene_atp_polymerization'][0]) - 1
            num_events += len(m['pointed_pyrene_adppi_polymerization'][0]) - 1
            num_events += len(m['pointed_pyrene_adp_polymerization'][0]) - 1
            num_events += len(m['pointed_adp_polymerization'][0]) - 1

            num_events += len(m['barbed_pyrene_atp_depolymerization'][0]) - 1
            num_events += len(m['barbed_pyrene_adppi_depolymerization'][0]) - 1
            num_events += len(m['barbed_pyrene_adp_depolymerization'][0]) - 1
            num_events += len(m['barbed_adp_depolymerization'][0]) - 1

            num_events += len(m['pointed_pyrene_atp_depolymerization'][0]) - 1
            num_events += len(m['pointed_pyrene_adppi_depolymerization'][0]) - 1
            num_events += len(m['pointed_pyrene_adp_depolymerization'][0]) - 1
            num_events += len(m['pointed_adp_depolymerization'][0]) - 1

            num_events += len(m['cleavage'][0]) - 1
            num_events += len(m['release'][0]) - 1
    return num_events
