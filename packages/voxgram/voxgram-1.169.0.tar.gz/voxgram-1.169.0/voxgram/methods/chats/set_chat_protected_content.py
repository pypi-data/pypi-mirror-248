from typing import Union

import voxgram
from voxgram import raw


class SetChatProtectedContent:
    async def set_chat_protected_content(
        self: "voxgram.Client",
        chat_id: Union[int, str],
        enabled: bool
    ) -> bool:
        await self.invoke(
            raw.functions.messages.ToggleNoForwards(
                peer=await self.resolve_peer(chat_id),
                enabled=enabled
            )
        )

        return True
