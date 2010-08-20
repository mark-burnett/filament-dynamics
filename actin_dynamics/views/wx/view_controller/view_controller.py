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

from .message_tracker import MessageTracker as _MessageTracker

from actin_dynamics.presenters import messages as presenter_messages
from actin_dynamics.view.wx import messages as view_messages

class ViewController(object):
    def __init__(self, trackers):
        self.trackers = trackers

    @classmethod
    def from_configobj(cls, publisher=None, configobj=None):
        trackers = []
        for section_name in configobj.sections():
            section = configobj[section_name]

            update_message = _get_object_from_module(
                    section['update_message'], section['update_message_module'])
            request_message = _get_object_from_module(
                    section['request_message'],
                    section['request_message_module'])

            trackers.append(_MessageTracker(publisher, update_message,
                                            update_message_field,
                                            request_message))
        return cls(trackers)

def _get_object_from_module(object_name, module_name):
    module = getattr(module_name, __module__)
    return getattr(object_name, module)
