import voxgram

from typing import List
from voxgram.types import Identifier, Listener

class GetManyListenersMatchingWithData:
    def get_many_listeners_matching_with_data(
        self: "voxgram.Client",
        data: Identifier,
        listener_type: "voxgram.enums.ListenerTypes",
    ) -> List[Listener]:
        listeners = []
        for listener in self.listeners[listener_type]:
            if listener.identifier.matches(data):
                listeners.append(listener)
        return listeners
