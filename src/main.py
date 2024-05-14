from typing import AsyncGenerator
from fastapi import Depends, FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from dependencies.template import get_template_response
from routes import partial_router
from settings import Settings
from contextlib import asynccontextmanager


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore[call-arg]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.settings = settings
    yield


app = FastAPI(title="Latex templates online", debug=settings.DEBUG, lifespan=lifespan)


app.mount("/static", StaticFiles(directory=settings.STATIC_PATH))
app.include_router(partial_router)


@app.get("/", response_class=HTMLResponse)
async def index(template_response=Depends(get_template_response)) -> Response:
    return template_response("index.html")


if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=settings.PORT, host=settings.HOST, reload=settings.DEBUG
    )
