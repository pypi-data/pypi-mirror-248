from typing import Callable

import voxgram


class OnDisconnect:
    def on_disconnect(self=None) -> Callable:
        def decorator(func: Callable) -> Callable:
            if isinstance(self, voxgram.Client):
                self.add_handler(voxgram.handlers.DisconnectHandler(func))
            else:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append((voxgram.handlers.DisconnectHandler(func), 0))

            return func

        return decorator
