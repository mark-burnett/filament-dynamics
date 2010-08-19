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

class Publisher(object):
    """
    Implements the observer design pattern.
    """
    __slots__ = ['registry', 'subclass_registry']
    def __init__(self):
        self.registry = collections.defaultdict(set)
        self.subclass_registry = collections.defaultdict(set)

    def subscribe(self, listener, message_type):
        """
        Adds a "listener" for messages of type "message_type."
        """
        if not callable(listener) or type == type(listener):
            raise RuntimeError('Invalid listener specified.')
        self.registry[message_type].add(listener)

    def subscribe_to_subclasses(self, listener, message_parent_type):
        """
        Adds "listener" for messages of all subclasses of "message_parent_type."
        """
        if not callable(listener) or type == type(listener):
            raise RuntimeError('Invalid listener specified.')
        self.subclass_registry[message_parent_type].add(listener)

    def unsubscribe(self, listener, message_type=None):
        """
        Removes "listener" from receiving messages of type "message_type."
        If "message_type" is None, removes "listener" from all types of messages.
        """
        if message_type:
            self.registry[message_type].discard(listener)
        else:
            for et in self.registry.keys():
                self.registry[et].discard(listener)

    def unsubscribe_from_subclasses(self, listener, message_parent_type=None):
        """
        Stop listening for subclasses of "message_parent_type."

        Removes only the direct subscription from that parent class.
        """
        if message_parent_type:
            self.subclass_registry[message_parent_type].discard(listener)
        else:
            for ept in self.subclass_registry.keys():
                self.subclass_registry[ept].discard(listener)

    def publish(self, message):
        """
        Send "message" to all appropriate listeners.
        """
        for l in self.registry[type(message)]:
            l(message)

        for ept in self.subclass_registry.keys():
            if isinstance(message, ept):
                for l in self.subclass_registry[ept]:
                    l(message)
