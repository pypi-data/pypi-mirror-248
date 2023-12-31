from typing import Union

import voxgram
from voxgram import raw


class GetBotInfo:
    async def get_bot_info(
        self: "voxgram.Client",
        lang_code: str,
        bot: Union[int, str] = None
    ) -> voxgram.types.BotInfo:
        peer = None
        if bot:
            peer = await self.resolve_peer(bot)
        r = await self.invoke(raw.functions.bots.GetBotInfo(lang_code=lang_code, bot=peer))
        return voxgram.types.BotInfo._parse(r)
