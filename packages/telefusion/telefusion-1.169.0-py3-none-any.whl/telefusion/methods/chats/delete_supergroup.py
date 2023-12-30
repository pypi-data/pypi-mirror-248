from typing import Union

import telefusion
from telefusion import raw


class DeleteSupergroup:
    async def delete_supergroup(
        self: "telefusion.Client",
        chat_id: Union[int, str]
    ) -> bool:
        await self.invoke(
            raw.functions.channels.DeleteChannel(
                channel=await self.resolve_peer(chat_id)
            )
        )

        return True
