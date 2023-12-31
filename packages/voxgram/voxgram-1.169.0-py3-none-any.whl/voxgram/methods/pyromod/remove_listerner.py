import voxgram
from voxgram.types import Listener

class RemoveListener:
    def remove_listener(
        self: "voxgram.Client",
        listener: Listener
    ):
        try:
            self.listeners[listener.listener_type].remove(listener)
        except ValueError:
            pass
