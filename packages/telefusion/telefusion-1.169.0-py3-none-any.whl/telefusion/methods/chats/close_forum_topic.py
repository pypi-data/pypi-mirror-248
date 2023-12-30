import telefusion
from telefusion import raw
from telefusion import types
from typing import Union


class CloseForumTopic:
    async def close_forum_topic(
        self: "telefusion.Client",
        chat_id: Union[int, str],
        topic_id: int
    ) -> bool:
        await self.invoke(
            raw.functions.channels.EditForumTopic(
                channel=await self.resolve_peer(chat_id),
                topic_id=topic_id,
                closed=True
            )
        )
        return True
