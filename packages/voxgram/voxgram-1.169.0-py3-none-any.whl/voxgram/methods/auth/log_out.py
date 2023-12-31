import logging

import voxgram
from voxgram import raw

log = logging.getLogger(__name__)


class LogOut:
    async def log_out(
        self: "voxgram.Client",
    ):
        await self.invoke(raw.functions.auth.LogOut())
        await self.stop()
        await self.storage.delete()

        return True
