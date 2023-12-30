from typing import Union

import telefusion
from telefusion import raw
from telefusion import types


class SetChatMenuButton:
    async def set_chat_menu_button(
        self: "telefusion.Client",
        chat_id: Union[int, str] = None,
        menu_button: "types.MenuButton" = None
    ) -> bool:
        await self.invoke(
            raw.functions.bots.SetBotMenuButton(
                user_id=await self.resolve_peer(chat_id or "me"),
                button=(
                    (await menu_button.write(self)) if menu_button
                    else (await types.MenuButtonDefault().write(self))
                )
            )
        )

        return True
