from typing import List

import voxgram
from voxgram import raw
from voxgram import types


class SetBotCommands:
    async def set_bot_commands(
        self: "voxgram.Client",
        commands: List["types.BotCommand"],
        scope: "types.BotCommandScope" = types.BotCommandScopeDefault(),
        language_code: str = "",
    ) -> bool:
        return await self.invoke(
            raw.functions.bots.SetBotCommands(
                commands=[c.write() for c in commands],
                scope=await scope.write(self),
                lang_code=language_code,
            )
        )
