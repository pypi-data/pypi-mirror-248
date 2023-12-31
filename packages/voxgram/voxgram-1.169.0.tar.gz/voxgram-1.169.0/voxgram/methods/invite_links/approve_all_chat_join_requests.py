from typing import Union

import voxgram
from voxgram import raw


class ApproveAllChatJoinRequests:
    async def approve_all_chat_join_requests(
        self: "voxgram.Client",
        chat_id: Union[int, str],
        invite_link: str = None
    ) -> bool:
        await self.invoke(
            raw.functions.messages.HideAllChatJoinRequests(
                peer=await self.resolve_peer(chat_id),
                approved=True,
                link=invite_link
            )
        )

        return True
