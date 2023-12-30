import telefusion
from telefusion import raw
from telefusion import types
from typing import Union


class UnhideGeneralTopic:
    async def unhide_general_topic(
        self: "telefusion.Client",
        chat_id: Union[int, str]
    ) -> bool:
        await self.invoke(
            raw.functions.channels.EditForumTopic(
                channel=await self.resolve_peer(chat_id),
                topic_id=1,
                hidden=False
            )
        )
        return True
