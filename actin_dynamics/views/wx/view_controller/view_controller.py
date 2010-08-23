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

import sys as _sys

from .message_tracker import MessageTracker as _MessageTracker

from actin_dynamics.presenters import messages as presenter_messages
from actin_dynamics.views.wx import messages as view_messages

class ViewController(object):
    def __init__(self, trackers):
        self.trackers = trackers

    @classmethod
    def from_configobj(cls, publisher=None, configobj=None):
        trackers = []
        message_tracker_config = configobj['message_trackers']
        for section_name in message_tracker_config.sections:
            section = message_tracker_config[section_name]

            update_message = _get_object_from_module(
                    section['update_message'], section['update_message_module'])
            request_message = _get_object_from_module(
                    section['request_message'],
                    section['request_message_module'])

            trackers.append(_MessageTracker(publisher, update_message,
                                            section['update_message_field'],
                                            request_message))
        return cls(trackers)

_this_module = _sys.modules[__name__]
def _get_object_from_module(object_name, module_name):
    module = getattr(_this_module, module_name)
    return getattr(module, object_name)
