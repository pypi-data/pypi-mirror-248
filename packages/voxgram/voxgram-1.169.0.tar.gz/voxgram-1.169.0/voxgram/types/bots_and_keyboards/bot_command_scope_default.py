import voxgram
from voxgram import raw
from .bot_command_scope import BotCommandScope


class BotCommandScopeDefault(BotCommandScope):
    def __init__(self):
        super().__init__("default")

    async def write(self, client: "voxgram.Client") -> "raw.base.BotCommandScope":
        return raw.types.BotCommandScopeDefault()
