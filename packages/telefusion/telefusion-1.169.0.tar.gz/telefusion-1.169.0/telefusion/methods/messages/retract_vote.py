from typing import Union

import telefusion
from telefusion import raw
from telefusion import types


class RetractVote:
    async def retract_vote(
        self: "telefusion.Client",
        chat_id: Union[int, str],
        message_id: int
    ) -> "types.Poll":
        r = await self.invoke(
            raw.functions.messages.SendVote(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                options=[]
            )
        )

        return types.Poll._parse(self, r.updates[0])
