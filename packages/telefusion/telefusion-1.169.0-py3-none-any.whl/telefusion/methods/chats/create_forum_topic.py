import telefusion
from telefusion import raw
from telefusion import types
from typing import Union


class CreateForumTopic:
    async def create_forum_topic(
        self: "telefusion.Client",
        chat_id: Union[int, str],
        title: str,
        icon_color: int = None,
        icon_emoji_id: int = None
    ) -> "types.ForumTopicCreated":
        r = await self.invoke(
            raw.functions.channels.CreateForumTopic(
                channel=await self.resolve_peer(chat_id),
                title=title,
                random_id=self.rnd_id(),
                icon_color=icon_color,
                icon_emoji_id=icon_emoji_id
            )
        )

        return types.ForumTopicCreated._parse(r.updates[1].message)
