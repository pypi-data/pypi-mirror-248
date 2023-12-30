import logging

import telefusion
from telefusion import raw
from telefusion.raw.core import TLObject
from telefusion.session import Session

log = logging.getLogger(__name__)


class Invoke:
    async def invoke(
        self: "telefusion.Client",
        query: TLObject,
        retries: int = Session.MAX_RETRIES,
        timeout: float = Session.WAIT_TIMEOUT,
        sleep_threshold: float = None
    ):
        if not self.is_connected:
            raise ConnectionError("Client has not been started yet")

        if self.no_updates:
            query = raw.functions.InvokeWithoutUpdates(query=query)

        if self.takeout_id:
            query = raw.functions.InvokeWithTakeout(takeout_id=self.takeout_id, query=query)

        r = await self.session.invoke(
            query, retries, timeout,
            (sleep_threshold
             if sleep_threshold is not None
             else self.sleep_threshold)
        )

        await self.fetch_peers(getattr(r, "users", []))
        await self.fetch_peers(getattr(r, "chats", []))

        return r
