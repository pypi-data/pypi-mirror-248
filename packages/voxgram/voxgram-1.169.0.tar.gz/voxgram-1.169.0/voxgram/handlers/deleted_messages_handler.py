from typing import List, Callable
import voxgram
from voxgram.filters import Filter
from voxgram.types import Message
from .handler import Handler

class DeletedMessagesHandler(Handler):
    def __init__(self, callback: Callable, filters: Filter = None):
        super().__init__(callback, filters)

    async def check(self, client: "voxgram.Client", messages: List[Message]):
        for message in messages:
            if await super().check(client, message):
                return True
        else:
            return False
