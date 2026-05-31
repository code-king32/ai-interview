from pydantic import BaseModel
from typing import Optional


class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str  # "seeker" | "hr"


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None
