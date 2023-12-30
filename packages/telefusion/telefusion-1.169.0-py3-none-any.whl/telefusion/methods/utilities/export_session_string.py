import telefusion


class ExportSessionString:
    async def export_session_string(
        self: "telefusion.Client"
    ):
        return await self.storage.export_session_string()
