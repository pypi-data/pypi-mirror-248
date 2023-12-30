import telefusion
from telefusion import raw
from telefusion import types


class GetMe:
    async def get_me(
        self: "telefusion.Client"
    ) -> "types.User":
        r = await self.invoke(
            raw.functions.users.GetFullUser(
                id=raw.types.InputUserSelf()
            )
        )

        users = {u.id: u for u in r.users}

        return types.User._parse(self, users[r.full_user.id])
