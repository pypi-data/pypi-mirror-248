from typing import Callable

import voxgram
from voxgram.filters import Filter


class OnChosenInlineResult:
    def on_chosen_inline_result(
        self=None,
        filters=None,
        group: int = 0
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            if isinstance(self, voxgram.Client):
                self.add_handler(voxgram.handlers.ChosenInlineResultHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        voxgram.handlers.ChosenInlineResultHandler(func, self),
                        group if filters is None else filters
                    )
                )

            return func

        return decorator
