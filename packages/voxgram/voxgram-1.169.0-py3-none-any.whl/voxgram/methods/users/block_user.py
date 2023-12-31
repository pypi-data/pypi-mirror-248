from typing import Union

import voxgram
from voxgram import raw


class BlockUser:
    async def block_user(
        self: "voxgram.Client",
        user_id: Union[int, str]
    ) -> bool:
        return bool(
            await self.invoke(
                raw.functions.contacts.Block(
                    id=await self.resolve_peer(user_id)
                )
            )
        )
