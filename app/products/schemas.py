from datetime import datetime

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    price: int = Field(ge=0, le=99999999)
    quantity: int = Field(1, ge=0, le=100000)
    created_at: datetime


class ProductUpdate(BaseModel):
    user_id: int | None = Field(None, gt=0)
    name: str | None = None
    price: int | None = Field(None, gt=0, le=99999999)
    quantity: int | None = Field(None, ge=0, le=100000)
