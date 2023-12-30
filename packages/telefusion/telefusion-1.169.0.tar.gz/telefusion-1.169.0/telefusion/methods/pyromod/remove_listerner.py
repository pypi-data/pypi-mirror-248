import telefusion
from telefusion.types import Listener

class RemoveListener:
    def remove_listener(
        self: "telefusion.Client",
        listener: Listener
    ):
        try:
            self.listeners[listener.listener_type].remove(listener)
        except ValueError:
            pass
