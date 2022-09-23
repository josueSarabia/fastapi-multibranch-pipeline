from fastapi import FastAPI
from .routes.images import routerImages
import uvicorn

app = FastAPI()


app.include_router(routerImages)

""" if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info") """
