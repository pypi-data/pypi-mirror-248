import os
import re
from typing import Union, Optional

import telefusion
from telefusion import raw
from telefusion import types
from telefusion.file_id import FileId


class CreateStickerSet:
    async def create_sticker_set(
        self: "telefusion.Client",
        user_id: Union[int, str],
        title: str,
        short_name: str,
        sticker: str,
        emoji: str = "🤔",
        masks: bool = None,
        animated: bool = None,
        videos: bool = None,
        emojis: bool = None
    ) -> Optional["types.Message"]:
        file = None

        if isinstance(sticker, str):
            if os.path.isfile(sticker) or re.match("^https?://", sticker):
                raise ValueError(f"file_id is invalid!")
            else:
                decoded = FileId.decode(sticker)
                media = raw.types.InputDocument(
                    id=decoded.media_id,
                    access_hash=decoded.access_hash,
                    file_reference=decoded.file_reference
                )
        else:
            raise ValueError(f"file_id is invalid!")

        r = await self.invoke(
            raw.functions.stickers.CreateStickerSet(
                user_id=await self.resolve_peer(user_id),
                title=title,
                short_name=short_name,
                stickers=[
                    raw.types.InputStickerSetItem(
                        document=media,
                        emoji=emoji
                    )
                ],
                masks=masks,
                animated=animated,
                videos=videos,
                emojis=emojis
            )
        )

        return types.StickerSet._parse(r.set)
