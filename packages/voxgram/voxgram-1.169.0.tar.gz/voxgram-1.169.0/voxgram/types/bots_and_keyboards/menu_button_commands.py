import voxgram
from voxgram import raw
from .menu_button import MenuButton


class MenuButtonCommands(MenuButton):
    def __init__(self):
        super().__init__("commands")

    async def write(self, client: "voxgram.Client") -> "raw.types.BotMenuButtonCommands":
        return raw.types.BotMenuButtonCommands()
