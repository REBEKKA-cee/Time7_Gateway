from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from time7_gateway.services.active_tags import ActiveTags
from time7_gateway.services.tag_info_cache import TagInfoCache

from time7_gateway.api.dashboard import router as dashboard_router
from time7_gateway.simulators.reader_route import router as reader_router



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

    # Routers
    app.include_router(reader_router, prefix="/api", tags=["reader"])
    app.include_router(dashboard_router, prefix="/api", tags=["dashboard"])

    @app.get("/health")
    def health():
        return {"ok": True}

    return app


app = create_app()