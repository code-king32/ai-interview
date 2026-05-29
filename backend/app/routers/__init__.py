from app.routers.jobs import router as jobs_router
from app.routers.candidates import router as candidates_router
from app.routers.interviews import router as interviews_router
from app.routers.reports import router as reports_router

__all__ = ["jobs_router", "candidates_router", "interviews_router", "reports_router"]