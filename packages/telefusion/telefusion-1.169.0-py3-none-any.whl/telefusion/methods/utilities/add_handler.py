import telefusion
from telefusion.handlers import DisconnectHandler
from telefusion.handlers.handler import Handler


class AddHandler:
    def add_handler(
        self: "telefusion.Client",
        handler: "Handler",
        group: int = 0
    ):
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = handler.callback
        else:
            self.dispatcher.add_handler(handler, group)

        return handler, group
