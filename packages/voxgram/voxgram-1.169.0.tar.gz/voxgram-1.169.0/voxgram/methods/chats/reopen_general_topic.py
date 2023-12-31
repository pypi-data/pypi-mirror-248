import voxgram
from voxgram import raw
from voxgram import types
from typing import Union


class ReopenGeneralTopic:
    async def reopen_general_topic(
        self: "voxgram.Client",
        chat_id: Union[int, str]
    ) -> bool:
        await self.invoke(
            raw.functions.channels.EditForumTopic(
                channel=await self.resolve_peer(chat_id),
                topic_id=1,
                closed=False
            )
        )
        return True
