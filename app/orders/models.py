from datetime import datetime

from auth.models import users
from products.models import products
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, MetaData, Table

orders_metadata = MetaData()
order_item_metadata = MetaData()

orders = Table(
    "orders",
    orders_metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id)),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
)

order_item = Table(
    "order_item",
    order_item_metadata,
    Column("id", Integer, primary_key=True),
    Column("order_id", Integer, ForeignKey(orders.c.id)),
    Column("product_id", Integer, ForeignKey(products.c.id)),
    Column("quantity", Integer, nullable=False),
)
