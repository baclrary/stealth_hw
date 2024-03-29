from typing import Optional

from fastapi_users import schemas


class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


# class UserUpdate(schemas.BaseUserUpdate):
#     pass
