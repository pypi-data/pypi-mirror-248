import logging
from typing import Union, Optional, AsyncGenerator

import telefusion
from telefusion import raw
from telefusion import types
from telefusion import utils

log = logging.getLogger(__name__)


class GetForumTopics:
    async def get_forum_topics(
        self: "telefusion.Client",
        chat_id: Union[int, str],
        limit: int = 0
    ) -> Optional[AsyncGenerator["types.ForumTopic", None]]:
        peer = await self.resolve_peer(chat_id)

        rpc = raw.functions.channels.GetForumTopics(channel=peer, offset_date=0, offset_id=0, offset_topic=0, limit=limit)

        r = await self.invoke(rpc, sleep_threshold=-1)

        for _topic in r.topics:
            yield types.ForumTopic._parse(_topic)
