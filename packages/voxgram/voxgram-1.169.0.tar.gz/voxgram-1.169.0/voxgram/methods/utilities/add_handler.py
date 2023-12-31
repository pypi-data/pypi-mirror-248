import voxgram
from voxgram.handlers import DisconnectHandler
from voxgram.handlers.handler import Handler


class AddHandler:
    def add_handler(
        self: "voxgram.Client",
        handler: "Handler",
        group: int = 0
    ):
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = handler.callback
        else:
            self.dispatcher.add_handler(handler, group)

        return handler, group
