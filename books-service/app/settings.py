"""Settings."""

from pydantic_settings import BaseSettings


class ServiceSettings(BaseSettings):
    """Service Settings."""

    environment: str = "local"
    service_name: str = "tepuii-api"


service_settings = ServiceSettings()
