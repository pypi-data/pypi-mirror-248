import telefusion

from typing import List
from telefusion.types import Identifier, Listener

class GetManyListenersMatchingWithData:
    def get_many_listeners_matching_with_data(
        self: "telefusion.Client",
        data: Identifier,
        listener_type: "telefusion.enums.ListenerTypes",
    ) -> List[Listener]:
        listeners = []
        for listener in self.listeners[listener_type]:
            if listener.identifier.matches(data):
                listeners.append(listener)
        return listeners
