from typing import List

import telefusion
from telefusion import raw
from telefusion import types


class GetDefaultEmojiStatuses:
    async def get_default_emoji_statuses(
        self: "telefusion.Client",
    ) -> List["types.EmojiStatus"]:
        r = await self.invoke(
            raw.functions.account.GetDefaultEmojiStatuses(hash=0)
        )

        return types.List([types.EmojiStatus._parse(self, i) for i in r.statuses])
