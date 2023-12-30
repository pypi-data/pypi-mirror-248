import telefusion
from telefusion import raw
from telefusion import types


class CreateSupergroup:
    async def create_supergroup(
        self: "telefusion.Client",
        title: str,
        description: str = ""
    ) -> "types.Chat":
        r = await self.invoke(
            raw.functions.channels.CreateChannel(
                title=title,
                about=description,
                megagroup=True
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
