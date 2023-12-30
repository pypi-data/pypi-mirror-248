from typing import Union

import telefusion
from telefusion import raw


class GetChatOnlineCount:
    async def get_chat_online_count(
        self: "telefusion.Client",
        chat_id: Union[int, str]
    ) -> int:
        return (await self.invoke(
            raw.functions.messages.GetOnlines(
                peer=await self.resolve_peer(chat_id)
            )
        )).onlines
