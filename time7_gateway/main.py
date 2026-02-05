from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from time7_gateway.services.active_tags import ActiveTags
from time7_gateway.services.tag_info_cache import TagInfoCache

from time7_gateway.api.dashboard import router as dashboard_router


from time7_gateway.api.reader import router as real_reader_router
from time7_gateway.simulators.reader_route import router as sim_reader_router


from time7_gateway.simulators.ias_services import mock_ias_lookup
from time7_gateway.clients.ias_services import ias_lookup as real_ias_lookup


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
    app.state.active_tags = ActiveTags(active_ttl_seconds=5)
    app.state.tag_info_cache = TagInfoCache(cache_ttl_hours=24)

    # IAS switch (mock vs real)
    # Use: IAS_MODE=mock or IAS_MODE=real
    ias_mode = os.getenv("IAS_MODE", "mock").strip().lower()
    app.state.ias_lookup = real_ias_lookup if ias_mode == "real" else mock_ias_lookup

    # Real reader endpoints
    app.include_router(real_reader_router, prefix="/api", tags=["reader-real"])

    # Simulator endpoints 
    app.include_router(sim_reader_router, prefix="/api/sim", tags=["reader-sim"])


    app.include_router(dashboard_router, prefix="/api", tags=["dashboard"])

    @app.get("/health")
    def health():
        return {"ok": True}

    return app


app = create_app()