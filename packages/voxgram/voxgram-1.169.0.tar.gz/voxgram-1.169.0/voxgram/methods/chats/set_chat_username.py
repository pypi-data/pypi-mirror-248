from typing import Union, Optional

import voxgram
from voxgram import raw


class SetChatUsername:
    async def set_chat_username(
        self: "voxgram.Client",
        chat_id: Union[int, str],
        username: Optional[str]
    ) -> bool:
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            return bool(
                await self.invoke(
                    raw.functions.channels.UpdateUsername(
                        channel=peer,
                        username=username or ""
                    )
                )
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user or chat')
