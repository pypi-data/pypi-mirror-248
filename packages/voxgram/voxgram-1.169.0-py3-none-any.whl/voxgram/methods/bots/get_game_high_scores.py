from typing import Union, List

import voxgram
from voxgram import raw
from voxgram import types


class GetGameHighScores:
    async def get_game_high_scores(
        self: "voxgram.Client",
        user_id: Union[int, str],
        chat_id: Union[int, str],
        message_id: int = None
    ) -> List["types.GameHighScore"]:
        r = await self.invoke(
            raw.functions.messages.GetGameHighScores(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                user_id=await self.resolve_peer(user_id)
            )
        )

        return types.List(types.GameHighScore._parse(self, score, r.users) for score in r.scores)
