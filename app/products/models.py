from datetime import datetime

from auth.models import users
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id)),
    Column("name", String, nullable=False),
    Column("price", Integer, nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
)
