# models.py
from dataclasses import dataclass
from typing import Optional
from typing import List


@dataclass
class IntentObject:
    intent_id: str
    expire_in: int
    purpose: str
    client_id: str
    redirect_uri: Optional[str]
    response_type: str
    scope: str
    intent_data: Optional[dict]

@dataclass
class TokenData:
    access_token: str
    refresh_token: str

@dataclass
class UserGroup:
    id: int
    name: str


@dataclass
class UserData:
    email: str
    email_verified: bool
    socian_id: str
    phone: str
    phone_verified: bool
    name: str
    gender: str
    avatar_url: str
    birth_date: str
    is_active: bool
    is_approved: bool
    date_joined: str
    groups: List[UserGroup]


@dataclass
class ApiResponse:
    message: str
    intent_object: Optional[IntentObject]
