from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from os import getcwd, path
from ..store.image_store import ImageStore


def get_store():
    images_path = path.join(getcwd(), "images")
    image_store = ImageStore(images_path)
    return image_store


routerImages = APIRouter()

@routerImages.post("/images/", status_code=201)
async def create_image(file: UploadFile, image_store: ImageStore = Depends(get_store)):

    if not file.filename.split(".")[1] == 'png':
        HTTPException(
            status_code=400,
            detail={
                "error": "invalid file",
                "detail": "image must be a .png"
            }
        )
    
    await image_store.save(file)
    return "success"


@routerImages.get("/images/{id}")
async def get_image(id: str):
    file_path = path.join(getcwd(), "images" , id + '.png')

    if not path.isfile(file_path):
        HTTPException(
            status_code=400,
            detail={
                "error": "invalid id",
                "detail": f"file not found with id {id}"
            }
        )
    return FileResponse(file_path)