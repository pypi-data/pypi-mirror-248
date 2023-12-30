import telefusion
from telefusion import raw
from .menu_button import MenuButton


class MenuButtonCommands(MenuButton):
    def __init__(self):
        super().__init__("commands")

    async def write(self, client: "telefusion.Client") -> "raw.types.BotMenuButtonCommands":
        return raw.types.BotMenuButtonCommands()
