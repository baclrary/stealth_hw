from auth.auth import current_active_user
from auth.manager import get_user_role_name
from auth.models import User
from auth.validators import validate_user_exists
from database import get_async_session
from fastapi import APIRouter, Depends, HTTPException, status
from products import crud
from products.permissions import is_admin_or_owner
from products.schemas import ProductCreate, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
async def get_products(session: AsyncSession = Depends(get_async_session)):
    return await crud.get_all_products(session)


@router.get("/{product_id}")
async def get_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    product = await crud.get_product_by_id(session, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("/")
async def add_product(
    new_product: ProductCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    role_name = await get_user_role_name(user.role_id, session)
    if role_name not in ["seller", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to add products")

    return await crud.create_product(session, new_product, user.id)


@router.patch("/{product_id}")
async def partial_update_product(
    product_id: int,
    updated_product: ProductUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    if not await is_admin_or_owner(user, product_id, session):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this product")

    if "user_id" in updated_product.model_dump(exclude_unset=True):
        if not await validate_user_exists(session, updated_product.user_id):
            raise HTTPException(status_code=400, detail="Invalid user_id provided")

    updated_product_record = await crud.update_product(session, product_id, updated_product)

    if updated_product_record:
        return {"status": "success", "updated_product": updated_product_record._asdict()}
    else:
        raise HTTPException(status_code=500, detail="Failed to update the product")


@router.delete("/{product_id}")
async def delete_product(
    product_id: int, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)
):
    if not await is_admin_or_owner(user, product_id, session):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this product")

    return await crud.delete_product(session, product_id)


# from auth.auth import current_active_user
# from auth.manager import get_user_role_name
# from auth.models import users
# from database import User, get_async_session
# from fastapi import APIRouter, Depends, HTTPException, status
# from products.models import products
# from products.permissions import is_admin_or_owner
# from products.schemas import ProductCreate, ProductUpdate
# from sqlalchemy import delete, insert, select, update
# from sqlalchemy.ext.asyncio import AsyncSession

# router = APIRouter(prefix="/products", tags=["Products"])


# @router.get("/")
# async def get_products(session: AsyncSession = Depends(get_async_session)):
#     query = select(products)
#     result = await session.execute(query)
#     return result.mappings().all()


# @router.get("/{product_id}")
# async def get_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
#     product = await session.execute(select(products).where(products.c.id == product_id))

#     if product.scalar_one_or_none() is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

#     result = await session.execute(select(products).where(products.c.id == product_id))
#     return result.mappings().all()


# @router.post("/")
# async def add_product(
#     new_product: ProductCreate,
#     session: AsyncSession = Depends(get_async_session),
#     user: User = Depends(current_active_user),
# ):
#     role_name = await get_user_role_name(user.role_id, session)
#     print(role_name)
#     if role_name not in ["seller", "admin"]:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to add products")

#     user_id = user.id
#     user_query = select(users).where(users.c.id == user_id)
#     user_result = await session.execute(user_query)
#     user_instance = user_result.scalars().first()

#     if not user_instance:
#         raise HTTPException(status_code=404, detail="User not found")

#     product_data = new_product.model_dump(exclude={"id"})
#     product_data["user_id"] = user_id

#     product_data = new_product.model_dump()
#     product_data["user_id"] = user_id

#     statement = insert(products).values(**product_data).returning(products)
#     res = await session.execute(statement)
#     await session.commit()

#     new_product_record = res.fetchone()

#     if new_product_record:
#         # Цікаво, а фронтам подобається стиль змінних пітоністів? Впевнений, що ні
#         # Навіть чув, що є бібліотека, яка снейк-кейс конвертує в кемел-кейс.
#         return {"status": "success", "created_product": new_product_record._asdict()}
#     else:
#         raise HTTPException(status_code=500, detail="Failed to create the product")


# @router.delete("/{product_id}")
# async def delete_product(
#     product_id: int, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)
# ):
#     if not await is_admin_or_owner(user, product_id, session):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this product")

#     product = await session.execute(select(products).where(products.c.id == product_id))

#     if product.scalar_one_or_none() is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

#     statement = delete(products).where(products.c.id == product_id)
#     await session.execute(statement)
#     await session.commit()

#     return {"status": "success", "message": f"Product with id {product_id} was deleted"}


# @router.patch("/{product_id}")
# async def partial_update_product(
#     product_id: int,
#     updated_product: ProductUpdate,
#     session: AsyncSession = Depends(get_async_session),
#     user: User = Depends(current_active_user),
# ):
#     if not await is_admin_or_owner(user, product_id, session):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this product")

#     product = await session.execute(select(products).where(products.c.id == product_id))

#     if product.scalar_one_or_none() is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

#     product_data = updated_product.model_dump(exclude_unset=True)
#     statement = update(products).where(products.c.id == product_id).values(**product_data).returning(products)
#     res = await session.execute(statement)
#     await session.commit()

#     updated_product_record = res.fetchone()

#     if updated_product_record:
#         return {"status": "success", "updated_product": updated_product_record._asdict()}
#     else:
#         raise HTTPException(status_code=500, detail="Failed to update the product")
