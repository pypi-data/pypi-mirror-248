import voxgram
from voxgram import raw
from voxgram import types


class CreateChannel:
    async def create_channel(
        self: "voxgram.Client",
        title: str,
        description: str = ""
    ) -> "types.Chat":
        r = await self.invoke(
            raw.functions.channels.CreateChannel(
                title=title,
                about=description,
                broadcast=True
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
