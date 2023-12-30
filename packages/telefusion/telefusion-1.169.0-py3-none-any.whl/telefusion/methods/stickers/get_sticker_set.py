import telefusion
from telefusion import raw
from telefusion import types


class GetStickerSet:
    async def get_sticker_set(
        self: "telefusion.Client",
        set_short_name: str
    ) -> "types.StickerSet":
        r = await self.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=set_short_name),
                hash=0
            )
        )

        return types.StickerSet._parse(r.set)
