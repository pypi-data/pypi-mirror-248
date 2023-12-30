from typing import List

import telefusion
from telefusion import raw
from telefusion import types


class ImportContacts:
    async def import_contacts(
        self: "telefusion.Client",
        contacts: List["types.InputPhoneContact"]
    ):
        imported_contacts = await self.invoke(
            raw.functions.contacts.ImportContacts(
                contacts=contacts
            )
        )

        return imported_contacts
