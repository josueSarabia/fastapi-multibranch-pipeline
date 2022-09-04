from genericpath import isdir
from uuid import uuid4
from os import path, mkdir

class ImageStore:

    def __init__(self, storage_path):
        self._storage_path = storage_path

    async def save(self, file):
        name = str(uuid4()) + ".png"
        newPath = path.join(self._storage_path, name)

        if not path.isdir(self._storage_path):
            mkdir(self._storage_path)

        with open(newPath, "wb") as newFile:
            content = await file.read()
            newFile.write(content)
            newFile.close()

        return name