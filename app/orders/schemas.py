from datetime import datetime

from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    user_id: int = Field(None, gt=0)
    created_at: datetime


class OrderUpdate(BaseModel):
    user_id: int | None = Field(None, gt=0)


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(1, ge=0, le=100000)


class OrderItemUpdate(BaseModel):
    product_id: int
    quantity: int = Field(1, ge=0, le=100000)
