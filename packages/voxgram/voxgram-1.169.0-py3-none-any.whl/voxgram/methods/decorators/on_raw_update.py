from typing import Callable

import voxgram


class OnRawUpdate:
    def on_raw_update(
        self=None,
        group: int = 0
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            if isinstance(self, voxgram.Client):
                self.add_handler(voxgram.handlers.RawUpdateHandler(func), group)
            else:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        voxgram.handlers.RawUpdateHandler(func),
                        group
                    )
                )

            return func

        return decorator
