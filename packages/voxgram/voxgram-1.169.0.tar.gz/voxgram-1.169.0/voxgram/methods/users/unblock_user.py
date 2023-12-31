from typing import Union

import voxgram
from voxgram import raw


class UnblockUser:
    async def unblock_user(
        self: "voxgram.Client",
        user_id: Union[int, str]
    ) -> bool:
        return bool(
            await self.invoke(
                raw.functions.contacts.Unblock(
                    id=await self.resolve_peer(user_id)
                )
            )
        )
