from typing import Union

import voxgram
from voxgram import raw


class DeleteChatAdminInviteLinks:
    async def delete_chat_admin_invite_links(
        self: "voxgram.Client",
        chat_id: Union[int, str],
        admin_id: Union[int, str],
    ) -> bool:
        return await self.invoke(
            raw.functions.messages.DeleteRevokedExportedChatInvites(
                peer=await self.resolve_peer(chat_id),
                admin_id=await self.resolve_peer(admin_id),
            )
        )
