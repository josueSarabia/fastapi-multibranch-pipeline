from fastapi import FastAPI
from .routes.images import routerImages

app = FastAPI()


app.include_router(routerImages)
