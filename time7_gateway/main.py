from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import asyncio
import os

from time7_gateway.clients.reader_client import run_reader_stream
from time7_gateway.services.active_tags import ActiveTags
from time7_gateway.services.tag_info_cache import TagInfoCache
from time7_gateway.api.dashboard import router as dashboard_router
from time7_gateway.simulators.ias_services import mock_ias_lookup
from time7_gateway.clients.ias_services import ias_lookup as real_ias_lookup

#for debug
from time7_gateway.debug.routes import router as debug_router

#terminal reader sim
from time7_gateway.simulators.reader_route import router as terminal_inject_router
#reader streamer sim
from time7_gateway.simulators.reader_streamer import router as reader_stream_router


load_dotenv()


def create_app() -> FastAPI:
    app = FastAPI(title="Time7 Gateway")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Shared in-memory state
    app.state.active_tags = ActiveTags(remove_grace_seconds=2.0)
    app.state.tag_info_cache = TagInfoCache(cache_ttl_hours=24)

    # IAS switch (mock vs real)
    ias_mode = os.getenv("IAS_MODE", "mock")
    app.state.ias_lookup = real_ias_lookup if ias_mode == "real" else mock_ias_lookup

    # Routers
    app.include_router(reader_stream_router, tags=["reader-stream-sim"])
    app.include_router(terminal_inject_router, prefix="/api/sim", tags=["reader-terminal-sim"])
    app.include_router(dashboard_router, prefix="/api", tags=["dashboard"])

    # Debug endpoints
    app.include_router(debug_router)

    @app.get("/health")
    def health():
        return {"ok": True}

    
    @app.on_event("startup")
    async def _start_reader_stream():
        asyncio.create_task(run_reader_stream(app))

    return app


app = create_app()