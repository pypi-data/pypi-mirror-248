from typing import Callable

import telefusion


class OnRawUpdate:
    def on_raw_update(
        self=None,
        group: int = 0
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            if isinstance(self, telefusion.Client):
                self.add_handler(telefusion.handlers.RawUpdateHandler(func), group)
            else:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        telefusion.handlers.RawUpdateHandler(func),
                        group
                    )
                )

            return func

        return decorator
