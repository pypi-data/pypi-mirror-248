import voxgram

from typing import List
from voxgram.types import Identifier, Listener

class GetManyListenersMatchingWithIdentifierPattern:
    def get_many_listeners_matching_with_identifier_pattern(
        self: "voxgram.Client",
        pattern: Identifier,
        listener_type: "voxgram.enums.ListenerTypes",
    ) -> List[Listener]:
        listeners = []
        for listener in self.listeners[listener_type]:
            if pattern.matches(listener.identifier):
                listeners.append(listener)
        return listeners
