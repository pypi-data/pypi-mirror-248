from typing import Union

import telefusion
from telefusion import raw


class UnpinAllChatMessages:
    async def unpin_all_chat_messages(
        self: "telefusion.Client",
        chat_id: Union[int, str],
    ) -> bool:
        await self.invoke(
            raw.functions.messages.UnpinAllMessages(
                peer=await self.resolve_peer(chat_id)
            )
        )

        return True
