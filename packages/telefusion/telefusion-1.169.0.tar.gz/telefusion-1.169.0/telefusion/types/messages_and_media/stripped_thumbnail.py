import telefusion
from telefusion import raw
from ..object import Object


class StrippedThumbnail(Object):
    def __init__(
        self,
        *,
        client: "telefusion.Client" = None,
        data: bytes
    ):
        super().__init__(client)

        self.data = data

    @staticmethod
    def _parse(client, stripped_thumbnail: "raw.types.PhotoStrippedSize") -> "StrippedThumbnail":
        return StrippedThumbnail(
            data=stripped_thumbnail.bytes,
            client=client
        )
