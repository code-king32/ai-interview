from app.routers.jobs import router as jobs_router
from app.routers.candidates import router as candidates_router
from app.routers.interviews import router as interviews_router
from app.routers.reports import router as reports_router
from app.routers.auth import router as auth_router
from app.routers.invite import router as invite_router
from app.routers.analytics import router as analytics_router
from app.routers.prompts import router as prompts_router

__all__ = ["jobs_router", "candidates_router", "interviews_router", "reports_router", "auth_router", "invite_router", "analytics_router", "prompts_router"]