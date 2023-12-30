import logging

import telefusion
from telefusion import raw
from telefusion import types

log = logging.getLogger(__name__)


class RecoverPassword:
    async def recover_password(
        self: "telefusion.Client",
        recovery_code: str
    ) -> "types.User":
        r = await self.invoke(
            raw.functions.auth.RecoverPassword(
                code=recovery_code
            )
        )

        await self.storage.user_id(r.user.id)
        await self.storage.is_bot(False)

        return types.User._parse(self, r.user)
