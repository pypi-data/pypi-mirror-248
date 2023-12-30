import telefusion


class Restart:
    async def restart(
        self: "telefusion.Client",
        block: bool = True
    ):
        async def do_it():
            await self.stop()
            await self.start()

        if block:
            await do_it()
        else:
            self.loop.create_task(do_it())

        return self
