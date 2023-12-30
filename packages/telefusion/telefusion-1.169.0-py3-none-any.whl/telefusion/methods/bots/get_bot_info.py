from typing import Union

import telefusion
from telefusion import raw


class GetBotInfo:
    async def get_bot_info(
        self: "telefusion.Client",
        lang_code: str,
        bot: Union[int, str] = None
    ) -> telefusion.types.BotInfo:
        peer = None
        if bot:
            peer = await self.resolve_peer(bot)
        r = await self.invoke(raw.functions.bots.GetBotInfo(lang_code=lang_code, bot=peer))
        return telefusion.types.BotInfo._parse(r)
