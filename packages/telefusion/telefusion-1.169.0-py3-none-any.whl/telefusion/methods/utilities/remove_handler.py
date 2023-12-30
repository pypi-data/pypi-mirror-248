import telefusion
from telefusion.handlers import DisconnectHandler
from telefusion.handlers.handler import Handler


class RemoveHandler:
    def remove_handler(
        self: "telefusion.Client",
        handler: "Handler",
        group: int = 0
    ):
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = None
        else:
            self.dispatcher.remove_handler(handler, group)
