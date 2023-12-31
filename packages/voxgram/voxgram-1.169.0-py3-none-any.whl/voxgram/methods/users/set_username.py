from typing import Optional

import voxgram
from voxgram import raw


class SetUsername:
    async def set_username(
        self: "voxgram.Client",
        username: Optional[str]
    ) -> bool:
        return bool(
            await self.invoke(
                raw.functions.account.UpdateUsername(
                    username=username or ""
                )
            )
        )
