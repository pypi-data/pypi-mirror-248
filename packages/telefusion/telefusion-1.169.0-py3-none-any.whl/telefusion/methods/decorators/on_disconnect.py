from typing import Callable

import telefusion


class OnDisconnect:
    def on_disconnect(self=None) -> Callable:
        def decorator(func: Callable) -> Callable:
            if isinstance(self, telefusion.Client):
                self.add_handler(telefusion.handlers.DisconnectHandler(func))
            else:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append((telefusion.handlers.DisconnectHandler(func), 0))

            return func

        return decorator
