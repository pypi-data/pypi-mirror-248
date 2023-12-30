from typing import List, Union

import telefusion
from telefusion import raw
from telefusion import utils
from telefusion.file_id import FileType


class DeleteProfilePhotos:
    async def delete_profile_photos(
        self: "telefusion.Client",
        photo_ids: Union[str, List[str]]
    ) -> bool:
        photo_ids = photo_ids if isinstance(photo_ids, list) else [photo_ids]
        input_photos = [utils.get_input_media_from_file_id(i, FileType.PHOTO).id for i in photo_ids]

        return bool(await self.invoke(
            raw.functions.photos.DeletePhotos(
                id=input_photos
            )
        ))
