import logging

import telefusion
from telefusion import raw

log = logging.getLogger(__name__)


class LogOut:
    async def log_out(
        self: "telefusion.Client",
    ):
        await self.invoke(raw.functions.auth.LogOut())
        await self.stop()
        await self.storage.delete()

        return True
