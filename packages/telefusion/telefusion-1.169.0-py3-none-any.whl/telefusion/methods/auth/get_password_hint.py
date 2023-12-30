import logging

import telefusion
from telefusion import raw

log = logging.getLogger(__name__)


class GetPasswordHint:
    async def get_password_hint(
        self: "telefusion.Client",
    ) -> str:
        return (await self.invoke(raw.functions.account.GetPassword())).hint
