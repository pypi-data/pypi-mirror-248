import telefusion
from telefusion import raw
from .bot_command_scope import BotCommandScope


class BotCommandScopeAllGroupChats(BotCommandScope):
    def __init__(self):
        super().__init__("all_group_chats")

    async def write(self, client: "telefusion.Client") -> "raw.base.BotCommandScope":
        return raw.types.BotCommandScopeChats()
