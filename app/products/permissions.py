from auth.models import User
from products.models import products
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def is_admin_or_owner(user: User, product_id: int, session: AsyncSession) -> bool:
    if user.is_superuser:
        return True

    product_query = select(products.c.user_id).where(products.c.id == product_id)
    product_result = await session.execute(product_query)
    product_user_id = product_result.scalar_one_or_none()

    if product_user_id is not None and product_user_id == user.id:
        return True
    return False
