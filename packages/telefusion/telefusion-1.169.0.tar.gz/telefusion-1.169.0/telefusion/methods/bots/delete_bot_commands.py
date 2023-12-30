import telefusion
from telefusion import raw, types


class DeleteBotCommands:
    async def delete_bot_commands(
        self: "telefusion.Client",
        scope: "types.BotCommandScope" = types.BotCommandScopeDefault(),
        language_code: str = "",
    ) -> bool:
        return await self.invoke(
            raw.functions.bots.ResetBotCommands(
                scope=await scope.write(self),
                lang_code=language_code,
            )
        )
