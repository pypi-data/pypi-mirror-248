import voxgram
from voxgram import raw
from ..object import Object


class MenuButton(Object):
    def __init__(self, type: str):
        super().__init__()

        self.type = type

    async def write(self, client: "voxgram.Client") -> "raw.base.BotMenuButton":
        raise NotImplementedError
