import voxgram
from voxgram import raw
from voxgram import types
from typing import Union


class DeleteForumTopic:
    async def delete_forum_topic(
        self: "voxgram.Client",
        chat_id: Union[int, str],
        topic_id: int
    ) -> bool:
        try:
            await self.invoke(
                raw.functions.channels.DeleteTopicHistory(
                    channel=await self.resolve_peer(chat_id),
                    top_msg_id=topic_id
                )
            )
        except Exception as e:
            print(e)
            return False
        return True
