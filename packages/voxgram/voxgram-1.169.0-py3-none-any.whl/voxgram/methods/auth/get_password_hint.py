import logging

import voxgram
from voxgram import raw

log = logging.getLogger(__name__)


class GetPasswordHint:
    async def get_password_hint(
        self: "voxgram.Client",
    ) -> str:
        return (await self.invoke(raw.functions.account.GetPassword())).hint
