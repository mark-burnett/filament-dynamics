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

import multiprocessing

from . import messages
from . import processing

class MultiprocessHandler(object):
    def __init__(self, publisher, num_processes=None):
        self.publisher = publisher
        self.revision = _get_revision()

        if num_processes:
            self.pool = multiprocessing.Pool(num_processes)
        else:
            self.pool = multiprocessing.Pool()

        self._subscribe_to_process_requests()

    def _subscribe_to_process_requests(self):
        self.publisher.subscribe(self.run_simulation,
                                 messages.RunSimulationRequest)

    def initialize(self):
        pass

    def terminate(self):
        try:
            self.pool.terminate()
        except:
            print 'Error ending process pool, trying again...'
            import time
            time.sleep(1)
            self.pool.terminate()
            print 'Process pool terminated.'


    def run_simulation(self, message):
        processing.run_simulation(message.sim_id, message.par_set_id,
                                  self.revision, message.num_runs, self.pool)

def _get_revision():
    from mercurial import hg, ui
    repository = hg.repository(ui.ui())
    return repository.filectx('gui.py', 'tip').rev()
