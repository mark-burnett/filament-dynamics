import collections

class Publisher(object):
    def __init__(self):
        self.registry = collections.defaultdict(set)

    def add(self, listener, event_type):
        """
        Adds a "listener" for events of type "event_type."
        """
        self.registry[event_type].add(listener)

    def remove(self, listener, event_type=None):
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
        for l in self.registry[type(event)]
            l(event)
