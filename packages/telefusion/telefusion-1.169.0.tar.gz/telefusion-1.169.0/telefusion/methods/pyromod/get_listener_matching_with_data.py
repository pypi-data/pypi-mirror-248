import telefusion

from typing import Optional
from telefusion.types import Identifier, Listener

class GetListenerMatchingWithData:
    def get_listener_matching_with_data(
        self: "telefusion.Client",
        data: Identifier,
        listener_type: "telefusion.enums.ListenerTypes"
    ) -> Optional[Listener]:
        matching = []
        for listener in self.listeners[listener_type]:
            if listener.identifier.matches(data):
                matching.append(listener)

        def count_populated_attributes(listener_item: Listener):
            return listener_item.identifier.count_populated()

        return max(matching, key=count_populated_attributes, default=None)
