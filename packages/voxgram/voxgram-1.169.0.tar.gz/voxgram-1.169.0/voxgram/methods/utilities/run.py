import asyncio
import inspect

import voxgram
from voxgram.methods.utilities.idle import idle


class Run:
    def run(
        self: "voxgram.Client",
        coroutine=None
    ):
        loop = asyncio.get_event_loop()
        run = loop.run_until_complete

        if coroutine is not None:
            run(coroutine)
        else:
            if inspect.iscoroutinefunction(self.start):
                run(self.start())
                run(idle())
                run(self.stop())
            else:
                self.start()
                run(idle())
                self.stop()
