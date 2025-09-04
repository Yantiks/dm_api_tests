from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Union

from pydantic import BaseModel, Field, ConfigDict


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class InfoBbText(BaseModel):
    value: str
    parseMode: List[BbParseMode]

class BbParseMode(str, Enum):
    COMMON = 'Common'
    INFO = 'Info'
    POST = 'Post'
    CHAT = 'Chat'

class ColorSchema(str, Enum):
    MODERN = 'Modern'
    PALE = 'Pale'
    CLASSIC = 'Classic'
    CLASSIC_PALE = 'ClassicPale'
    NIGHT = 'Night'

class PagingSettings(BaseModel):
    postsPerPage: int
    commentsPerPage: int
    topicsPerPage: int
    messagesPerPage: int
    entitiesPerPage: int


class UserSettings(BaseModel):
    colorSchema: ColorSchema
    nannyGreetingsMessage: str = Field(None, alias = 'nannyGreetingsMessage')
    paging: PagingSettings

class Metadata(BaseModel):
    email: str | None = None

class UserRole(str, Enum):
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNY_MODERATOR = 'NannyModerator'
    REGULAR_MODERATOR = 'RegularModerator'
    SENIOR_MODERATOR = 'SeniorModerator'

class Userdetails(BaseModel):
    login: str
    roles: List[UserRole]
    mediumPictureUrl: str = Field(None, alias='mediumPictureUrl')
    smallPictureUrl: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None, alias='status')
    rating: Rating
    online: datetime = Field(None, alias='online')
    name: str = Field(None, alias='name')
    location: str = Field(None, alias='location')
    registration: datetime = Field(None, alias='registration')
    icq: str = Field(None, alias='icq')
    skype: str = Field(None, alias='skype')
    originalPictureUrl: str = Field(None, alias='originalPictureUrl')
    info: Union[InfoBbText, str] = Field(None, alias='info')
    settings: UserSettings


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Userdetails
    metadata: Metadata | str | None = Field(None, alias='metadata')
