import voxgram
from voxgram.handlers import DisconnectHandler
from voxgram.handlers.handler import Handler


class RemoveHandler:
    def remove_handler(
        self: "voxgram.Client",
        handler: "Handler",
        group: int = 0
    ):
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = None
        else:
            self.dispatcher.remove_handler(handler, group)
