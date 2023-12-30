import telefusion

from typing import Optional
from telefusion.types import Identifier, Listener

class GetListenerMatchingWithIdentifierPattern:
    def get_listener_matching_with_identifier_pattern(
        self: "telefusion.Client",
        pattern: Identifier,
        listener_type: "telefusion.enums.ListenerTypes"
    ) -> Optional[Listener]:
        matching = []
        for listener in self.listeners[listener_type]:
            if pattern.matches(listener.identifier):
                matching.append(listener)

        def count_populated_attributes(listener_item: Listener):
            return listener_item.identifier.count_populated()

        return max(matching, key=count_populated_attributes, default=None)
