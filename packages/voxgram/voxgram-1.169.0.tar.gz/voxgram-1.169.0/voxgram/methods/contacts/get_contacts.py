import logging
from typing import List

import voxgram
from voxgram import raw
from voxgram import types

log = logging.getLogger(__name__)


class GetContacts:
    async def get_contacts(
        self: "voxgram.Client"
    ) -> List["types.User"]:
        contacts = await self.invoke(raw.functions.contacts.GetContacts(hash=0))
        return types.List(types.User._parse(self, user) for user in contacts.users)
