from typing import Optional

import voxgram
from voxgram import raw, types


class SetEmojiStatus:
    async def set_emoji_status(
        self: "voxgram.Client",
        emoji_status: Optional["types.EmojiStatus"] = None
    ) -> bool:
        await self.invoke(
            raw.functions.account.UpdateEmojiStatus(
                emoji_status=(
                    emoji_status.write()
                    if emoji_status
                    else raw.types.EmojiStatusEmpty()
                )
            )
        )

        return True
