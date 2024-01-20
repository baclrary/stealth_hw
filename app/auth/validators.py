from auth.models import users
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def validate_user_exists(session: AsyncSession, user_id: int) -> bool:
    """Validate if a user exists in the database."""
    user_query = select(users).where(users.c.id == user_id)
    user_result = await session.execute(user_query)
    if user_result.scalar_one_or_none() is None:
        return False
    return True
