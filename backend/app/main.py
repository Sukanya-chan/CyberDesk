"""CyberDesk FastAPI application entrypoint."""
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.learning import router as learning_router
from app.api.admin_learning import router as admin_learning_router
from app.api.assessment import router as assessment_router
from app.api.admin_assessment import router as admin_assessment_router
from app.api.challenges import router as challenges_router
from app.api.admin_challenges import router as admin_challenges_router
from app.core.config import get_settings
from app.db.session import Base, engine

# Import models so they register on Base.metadata before create_all().
# Phase 2 introduces the first real table (AppUser); no migration tool is
# in place yet (SQLite MVP, per context/Decisions.md ADR-002), so this is
# the same "create tables that don't exist" pattern used for the earlier
# connectivity check.
import app.models  # noqa: E402,F401

logger = logging.getLogger("cyberdesk")
logging.basicConfig(level=logging.INFO)

settings = get_settings()

app = FastAPI(title=settings.app_name)

# SQLite MVP: create any tables that don't exist yet. Never drops or
# alters existing tables, so this is safe to run on every startup.
Base.metadata.create_all(bind=engine)

# CORS: only the configured local frontend origin(s) are allowed.
# No wildcard origin is used, even in development, to keep the
# configuration safe to carry forward.
allowed_origins = [
    origin.strip()
    for origin in settings.cors_allowed_origins.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Return a consistent JSON error shape for HTTP errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"message": exc.detail, "status_code": exc.status_code}},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Return a consistent JSON error shape for request validation errors."""
    return JSONResponse(
        status_code=422,
        content={"error": {"message": "Invalid request", "details": exc.errors()}},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler that never leaks internals to the client."""
    logger.exception("Unhandled exception while processing request")
    return JSONResponse(
        status_code=500,
        content={"error": {"message": "Internal server error"}},
    )


app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(learning_router, prefix="/api")
app.include_router(admin_learning_router, prefix="/api")
app.include_router(assessment_router, prefix="/api")
app.include_router(admin_assessment_router, prefix="/api")
app.include_router(challenges_router, prefix="/api")
app.include_router(admin_challenges_router, prefix="/api")
