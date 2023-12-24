from typing import Any

from fastapi import FastAPI

from speech_recognition_api.core.async_api.async_api import async_router
from speech_recognition_api.core.sync_api.sync_api import sync_router


def create_app(**fastapi_kwargs: Any) -> FastAPI:  # noqa: ANN401
    if "title" not in fastapi_kwargs:
        fastapi_kwargs["title"] = "Speech Recognition API"

    if "description" not in fastapi_kwargs:
        fastapi_kwargs["description"] = "Simple but extensible API for Speech Recognition."

    if "version" not in fastapi_kwargs:
        fastapi_kwargs["version"] = "0.1.0"

    app = FastAPI(**fastapi_kwargs)
    app.include_router(sync_router)
    app.include_router(async_router)
    return app
