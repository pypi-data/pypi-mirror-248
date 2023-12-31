from typing import List

import voxgram
from voxgram import raw
from voxgram import types


class ImportContacts:
    async def import_contacts(
        self: "voxgram.Client",
        contacts: List["types.InputPhoneContact"]
    ):
        imported_contacts = await self.invoke(
            raw.functions.contacts.ImportContacts(
                contacts=contacts
            )
        )

        return imported_contacts
