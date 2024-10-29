from pathlib import Path
from PIL import Image, UnidentifiedImageError
import shutil
from schemas.settings import STATIC_DIRECTORY
from fastapi import UploadFile

from exception import ImageErrorException



def image_upload(file_location: Path, file: UploadFile) -> str:
    try:
        image = Image.open(file.file)
        image.verify()
    except UnidentifiedImageError:
        raise ImageErrorException("Invalid image uploaded")
    
    # reset image ...
    file.file.seek(0)

    file_location.mkdir(exist_ok=True, parents=True)


    file_loc = file_location / file.filename

    with open(file_loc, "wb") as image_f:
        shutil.copyfileobj(file.file, image_f)
    
    relative_path = file_loc.relative_to(STATIC_DIRECTORY.parent)

    return str(relative_path)

