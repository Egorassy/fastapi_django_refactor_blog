from pydantic import BaseModel, Field, field_validator
from typing import Annotated


class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    first_name: Annotated[str, Field(min_length=1, max_length=100)]
    last_name: Annotated[str, Field(min_length=1, max_length=100)]
    nickname: Annotated[str, Field(min_length=3, max_length=50)]
    email: Annotated[str, Field(min_length=5, max_length=255)]
    password: Annotated[str, Field(min_length=8, max_length=128)]

    @field_validator("email")
    def email_must_look_like_email(cls, v: str):
        value = v.strip()
        if "@" not in value or " " in value:
            raise ValueError("Invalid email")
        return value


class UserEdit(BaseModel):
    username: Annotated[str | None, Field(min_length=3, max_length=50)] = None
    first_name: Annotated[str | None, Field(min_length=1, max_length=100)] = None
    last_name: Annotated[str | None, Field(min_length=1, max_length=100)] = None
    nickname: Annotated[str | None, Field(min_length=3, max_length=50)] = None
    email: Annotated[str | None, Field(min_length=5, max_length=255)] = None

    @field_validator("email")
    def email_must_look_like_email(cls, v: str | None):
        if v is None:
            return v
        value = v.strip()
        if "@" not in value or " " in value:
            raise ValueError("Invalid email")
        return value


class UserRead(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    nickname: str

    class Config:
        from_attributes = True


class UserEditRead(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    nickname: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True
