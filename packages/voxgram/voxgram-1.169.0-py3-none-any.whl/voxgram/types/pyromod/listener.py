from asyncio import Future
from dataclasses import dataclass
from typing import Callable

import voxgram

from .identifier import Identifier

@dataclass
class Listener:
    listener_type: voxgram.enums.ListenerTypes
    filters: "voxgram.filters.Filter"
    unallowed_click_alert: bool
    identifier: Identifier
    future: Future = None
    callback: Callable = None
