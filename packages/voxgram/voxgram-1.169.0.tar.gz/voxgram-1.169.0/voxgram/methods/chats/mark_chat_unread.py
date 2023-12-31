from typing import Union

import voxgram
from voxgram import raw


class MarkChatUnread:
    async def mark_chat_unread(
        self: "voxgram.Client",
        chat_id: Union[int, str],
    ) -> bool:
        return await self.invoke(
            raw.functions.messages.MarkDialogUnread(
                peer=await self.resolve_peer(chat_id),
                unread=True
            )
        )
