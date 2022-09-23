import pytest
from unittest.mock import AsyncMock
from ..store.image_store import ImageStore
from fastapi.testclient import TestClient
from ..main import app
from ..routes.images import get_store
from os import path, getcwd, remove, rmdir
from fastapi import UploadFile


pytest_plugins = ("pytest_asyncio",)

async def save():
    return ""

@pytest.fixture
def mock_store():
    store = ImageStore('fake_store')
    return AsyncMock(store)

@pytest.fixture
def client(mock_store):
    mock_store.save.return_value = ""
    app.dependency_overrides[get_store] = lambda: mock_store
    return TestClient(app)


def test_post_image(client, mock_store):
    file_path = path.join(getcwd(), "src", "tests" ,"resources", "img_avatar.png")
    with open(file_path, "rb") as f:
        response = client.post(f"/images/?args=None&kwargs=None", files={'file': f})

        print(response.json(), 'responseeee')
        assert response.status_code == 201

        assert response.json() == "success"


@pytest.mark.asyncio
async def test_saving_image():

    fake_uuid = "123e4567-e89b-12d3-a456-426655440000"
    def mock_uuidgen():
        return fake_uuid

    file_path = path.join(getcwd(), "src", "tests" ,"resources", "img_avatar.png")
    with open(file_path, "rb") as f:
        fake_request_stream = UploadFile(filename='test_name', file=f, content_type="image/png")

        storage_path = "fake-storage-path"
        store = ImageStore(
            storage_path
        )

        assert await store.save(fake_request_stream, mock_uuidgen) == fake_uuid + ".png"
    remove(path.join(getcwd(), "fake-storage-path", fake_uuid + ".png"))
    rmdir(path.join(getcwd(), "fake-storage-path"))
