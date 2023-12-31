import voxgram


class ExportSessionString:
    async def export_session_string(
        self: "voxgram.Client"
    ):
        return await self.storage.export_session_string()
