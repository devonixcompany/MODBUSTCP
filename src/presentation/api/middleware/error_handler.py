"""Error handling middleware for FastAPI."""

import logging
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for centralized error handling."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Handle requests and catch unhandled exceptions."""
        try:
            response = await call_next(request)
            return response
            
        except Exception as e:
            logger.error(f"Unhandled exception in API: {e}", exc_info=True)
            
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                    "detail": str(e) if request.app.state.config.debug else None
                }
            )