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

import collections

# XXX Consider adding a way to subscribe_all (adding a separate registry)
# XXX Consider supporting a co-publisher?
class Publisher(object):
    __slots__ = ['registry']
    def __init__(self):
        self.registry = collections.defaultdict(set)

    def subscribe(self, listener, event_type):
        """
        Adds a "listener" for events of type "event_type."
        """
        assert(callable(listener))
        self.registry[event_type].add(listener)

    def unsubscribe(self, listener, event_type=None):
        """
        Removes "listener" from receiving events of type "event_type."
        If "event_type" is None, removes "listener" from all types of events.
        """
        if event_type:
            self.registry[event_type].discard(listener)
        else:
            for et in self.registry.keys():
                self.registry[et].discard(listener)

    def publish(self, event):
        """
        Send "event" to all appropriate listeners.
        """
        for l in self.registry[type(event)]:
            l(event)

    @property
    def events(self):
        return self.registry.keys()
