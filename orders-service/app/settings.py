"""Settings."""

from pydantic_settings import BaseSettings


class ServiceSettings(BaseSettings):
    """Service Settings."""

    environment: str = "local"
    service_name: str = "orders-service"


class BooksServiceSettings(BaseSettings):
    """Books Service Settings."""

    api_url: str = "http://books-service:80"
    timeout: int = 5


book_service_setting = BooksServiceSettings()
service_settings = ServiceSettings()
