import telefusion

from telefusion.filters import Filter
from typing import Callable, List, Optional, Union
from telefusion.types import Identifier, Listener

class RegisterNextStepHandler:
    def register_next_step_handler(
        self: "telefusion.Client",
        callback: Callable,
        filters: Optional[Filter] = None,
        listener_type: "telefusion.enums.ListenerTypes" = telefusion.enums.ListenerTypes.MESSAGE,
        unallowed_click_alert: bool = True,
        chat_id: Union[Union[int, str], List[Union[int, str]]] = None,
        user_id: Union[Union[int, str], List[Union[int, str]]] = None,
        message_id: Union[int, List[int]] = None,
        inline_message_id: Union[str, List[str]] = None,
    ):
        pattern = Identifier(
            from_user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )

        listener = Listener(
            callback=callback,
            filters=filters,
            unallowed_click_alert=unallowed_click_alert,
            identifier=pattern,
            listener_type=listener_type,
        )

        self.listeners[listener_type].append(listener)
