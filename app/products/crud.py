from products.models import products
from products.schemas import ProductCreate, ProductUpdate
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_products(session: AsyncSession):
    """Retrieve all products."""
    result = await session.execute(select(products))
    return result.mappings().all()


async def get_product_by_id(session: AsyncSession, product_id: int):
    """Retrieve a product by its ID."""
    result = await session.execute(select(products).where(products.c.id == product_id))
    return result.mappings().first()


async def create_product(session: AsyncSession, product_data: ProductCreate, user_id: int):
    """Create a new product."""
    new_product = product_data.model_dump()
    new_product["user_id"] = user_id
    statement = insert(products).values(**new_product).returning(products)
    result = await session.execute(statement)
    await session.commit()

    new_product_record = result.fetchone()
    return new_product_record._asdict() if new_product_record else None


async def update_product(session: AsyncSession, product_id: int, product_data: ProductUpdate):
    """Update an existing product."""
    update_data = product_data.model_dump(exclude_unset=True)
    statement = update(products).where(products.c.id == product_id).values(**update_data).returning(products)
    result = await session.execute(statement)
    await session.commit()
    return result.fetchone()


async def delete_product(session: AsyncSession, product_id: int):
    """Delete a product."""
    statement = delete(products).where(products.c.id == product_id)
    await session.execute(statement)
    await session.commit()
    return {"status": "success", "message": f"Product with id {product_id} was deleted"}
