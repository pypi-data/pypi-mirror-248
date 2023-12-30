import logging

import telefusion
from telefusion import raw

log = logging.getLogger(__name__)


class SendRecoveryCode:
    async def send_recovery_code(
        self: "telefusion.Client",
    ) -> str:
        return (await self.invoke(
            raw.functions.auth.RequestPasswordRecovery()
        )).email_pattern
