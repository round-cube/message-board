from fastapi import FastAPI

from mb.settings import Settings
from mb.storage import Storage
from mb.login.views import router as login_router
from mb.posts.views import router as posts_router


def get_app() -> FastAPI:
    app = FastAPI()
    app.storage = Storage()
    app.settings = Settings(_env_file=".env")
    app.include_router(login_router)
    app.include_router(posts_router)
    return app


app = get_app()
