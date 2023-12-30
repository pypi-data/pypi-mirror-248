import telefusion

from typing import List
from telefusion.types import Identifier, Listener

class GetManyListenersMatchingWithIdentifierPattern:
    def get_many_listeners_matching_with_identifier_pattern(
        self: "telefusion.Client",
        pattern: Identifier,
        listener_type: "telefusion.enums.ListenerTypes",
    ) -> List[Listener]:
        listeners = []
        for listener in self.listeners[listener_type]:
            if pattern.matches(listener.identifier):
                listeners.append(listener)
        return listeners
