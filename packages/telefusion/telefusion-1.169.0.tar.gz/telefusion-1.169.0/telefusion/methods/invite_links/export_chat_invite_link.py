from typing import Union

import telefusion
from telefusion import raw
from telefusion import types


class ExportChatInviteLink:
    async def export_chat_invite_link(
        self: "telefusion.Client",
        chat_id: Union[int, str],
    ) -> "types.ChatInviteLink":
        r = await self.invoke(
            raw.functions.messages.ExportChatInvite(
                peer=await self.resolve_peer(chat_id),
                legacy_revoke_permanent=True
            )
        )

        return r.link
