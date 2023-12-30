import inspect
import telefusion

from telefusion.errors import ListenerStopped
from telefusion.types import Listener
from telefusion.utils import PyromodConfig

class StopListener:
    async def stop_listener(
        self: "telefusion.Client",
        listener: Listener
    ):
        self.remove_listener(listener)

        if listener.future.done():
            return

        if callable(PyromodConfig.stopped_handler):
            if inspect.iscoroutinefunction(PyromodConfig.stopped_handler.__call__):
                await PyromodConfig.stopped_handler(None, listener)
            else:
                await self.loop.run_in_executor(
                    None, PyromodConfig.stopped_handler, None, listener
                )
        elif PyromodConfig.throw_exceptions:
            listener.future.set_exception(ListenerStopped())
