from pydantic import BaseModel, HttpUrl, validator
from typing import Optional, List
from datetime import datetime
from enum import IntEnum
from decimal import Decimal


class Status(IntEnum):
    ACTIVE = 0
    PAUSED = 1
    COMPLETED = 2
    ERROR = 3


class Platform(IntEnum):
    TWITTER = 0
    TELEGRAM = 1
    WEB = 2


class ActionType(IntEnum):
    FOLLOW = 0
    ACTION = 1
    COMMENT = 2


class FetchedTask(BaseModel):
    id: int
    type: ActionType
    platform: Platform
    name: str
    key_action: str
    url: HttpUrl
    description: Optional[str] = None
    image_url: Optional[str] = None

    @validator("type", pre=True)
    def validate_type(cls, value):
        if isinstance(value, str):
            return ActionType[value]
        return ActionType(value)

    @validator("platform", pre=True)
    def validate_platform(cls, value):
        if isinstance(value, str):
            return Platform[value]
        return Platform(value)

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: float,
            ActionType: lambda v: v.name,
            Platform: lambda v: v.name,
        }


class PerformanceStats(BaseModel):
    impressions: int
    conversions: int


class TaskPerformance(BaseModel):
    task: PerformanceStats
    app: PerformanceStats


class StatsChangeSuccessResponse(BaseModel):
    status_code: int
    initial: TaskPerformance
    changed: TaskPerformance
    debug: bool


class FetchedTaskResponse(BaseModel):
    tasks: List[FetchedTask]
    total: int
    expiration: datetime


class AdsClientOptions(BaseModel):
    quantity: int = 5
    expiration_time_in_hours: int = 48
    platform: List[Platform] = [Platform.TWITTER, Platform.TELEGRAM, Platform.WEB]
    action_type: List[ActionType] = [
        ActionType.FOLLOW,
        ActionType.ACTION,
        ActionType.COMMENT,
    ]
    status: List[Status] = [Status.ACTIVE]
    free: bool = False
    debug_mode: bool = True

    class Config:
        json_encoders = {
            Decimal: float,
            ActionType: lambda v: v.value,
            Platform: lambda v: v.value,
            Status: lambda v: v.value,
        }
