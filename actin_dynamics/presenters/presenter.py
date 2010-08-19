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

from . import messages

class Presenter(object):
    def __init__(self, publisher=None, handlers=None):
        self.publisher = publisher
        self.handlers = handlers

        self._subscribe_to_core_requests()

    def initialize(self):
        for h in self.handlers:
            h.initialize()

    def _subscribe_to_core_requests(self):
        self.publisher.subscribe(self.exit_program, messages.ExitProgram)

    def exit_program(self, message):
        for h in self.handlers:
            h.terminate()

        from twisted.internet import reactor
        reactor.stop()
