from typing import Optional

import telefusion
from telefusion import raw


class SetUsername:
    async def set_username(
        self: "telefusion.Client",
        username: Optional[str]
    ) -> bool:
        return bool(
            await self.invoke(
                raw.functions.account.UpdateUsername(
                    username=username or ""
                )
            )
        )
