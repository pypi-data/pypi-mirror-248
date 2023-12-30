import telefusion

from ..object import Object


class InputMessageContent(Object):
    def __init__(self):
        super().__init__()

    async def write(self, client: "telefusion.Client", reply_markup):
        raise NotImplementedError
