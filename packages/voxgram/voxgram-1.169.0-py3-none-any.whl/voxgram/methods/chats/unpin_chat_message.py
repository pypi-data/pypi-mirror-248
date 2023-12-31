from typing import Union

import voxgram
from voxgram import raw


class UnpinChatMessage:
    async def unpin_chat_message(
        self: "voxgram.Client",
        chat_id: Union[int, str],
        message_id: int = 0
    ) -> bool:
        await self.invoke(
            raw.functions.messages.UpdatePinnedMessage(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                unpin=True
            )
        )

        return True
