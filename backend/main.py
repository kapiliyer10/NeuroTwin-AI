from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import ingest, recommend, simulate, state
from backend.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Digital cognitive twin API for signal ingestion, state estimation, simulation, and recommendations.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(ingest.router)
    app.include_router(state.router)
    app.include_router(simulate.router)
    app.include_router(recommend.router)
    return app


app = create_app()
