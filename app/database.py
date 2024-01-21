from typing import AsyncGenerator

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def init_db():
    """Initialize the database with predefined values."""
    session = AsyncSession(bind=engine, expire_on_commit=False)
    try:
        # Check if roles already exist to avoid duplication
        result = await session.execute(text("SELECT 1 FROM roles WHERE id IN (1, 2, 3)"))
        if not result.scalars().first():
            # Insert roles if they don't exist
            await session.execute(
                text("INSERT INTO roles (id, name) VALUES (1, 'admin'), (2, 'customer'), (3, 'seller')")
            )
            await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()
