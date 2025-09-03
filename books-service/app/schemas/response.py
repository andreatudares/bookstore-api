"""Response Schemas."""

import datetime

from pydantic import BaseModel, Field


class ErrorDetailModel(BaseModel):
    """Error Detail Model."""

    field: str
    issue: str


class ResponseModel(BaseModel):
    """Response Model."""

    success: bool
    message: str
    data: BaseModel | None = None
    errors: list[ErrorDetailModel] | None = None
    timestamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
