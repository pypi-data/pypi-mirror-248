from typing import List, Callable
import telefusion
from telefusion.filters import Filter
from telefusion.types import Message
from .handler import Handler

class DeletedMessagesHandler(Handler):
    def __init__(self, callback: Callable, filters: Filter = None):
        super().__init__(callback, filters)

    async def check(self, client: "telefusion.Client", messages: List[Message]):
        for message in messages:
            if await super().check(client, message):
                return True
        else:
            return False
