from typing import Union

import voxgram
from voxgram import raw
from voxgram import types


class ExportChatInviteLink:
    async def export_chat_invite_link(
        self: "voxgram.Client",
        chat_id: Union[int, str],
    ) -> "types.ChatInviteLink":
        r = await self.invoke(
            raw.functions.messages.ExportChatInvite(
                peer=await self.resolve_peer(chat_id),
                legacy_revoke_permanent=True
            )
        )

        return r.link
