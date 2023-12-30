from typing import Callable

import telefusion
from telefusion.filters import Filter


class OnUserStatus:
    def on_user_status(
        self=None,
        filters=None,
        group: int = 0
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            if isinstance(self, telefusion.Client):
                self.add_handler(telefusion.handlers.UserStatusHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        telefusion.handlers.UserStatusHandler(func, self),
                        group if filters is None else filters
                    )
                )

            return func

        return decorator
