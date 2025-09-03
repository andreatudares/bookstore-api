"""Main."""

from mangum import Mangum

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import exceptions
from app.routers import orders_router
from app.settings import service_settings

app = FastAPI(
    docs_url="/docs" if service_settings.environment == "local" else None,
    redoc_url="/redoc" if service_settings.environment == "local" else None,
)


app.include_router(router=orders_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # This allows all origins for development. Adjust it for production.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods.
    allow_headers=["*"],  # Allows all headers.
)
app.add_exception_handler(
    exc_class_or_status_code=Exception,
    handler=exceptions.CustomExceptionHandler.handle_exception,
)


handler = Mangum(app=app)
