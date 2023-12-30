from asyncio import Future
from dataclasses import dataclass
from typing import Callable

import telefusion

from .identifier import Identifier

@dataclass
class Listener:
    listener_type: telefusion.enums.ListenerTypes
    filters: "telefusion.filters.Filter"
    unallowed_click_alert: bool
    identifier: Identifier
    future: Future = None
    callback: Callable = None
