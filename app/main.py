from auth.auth import auth_backend, fastapi_users
from auth.schemas import UserCreate, UserRead
from fastapi import FastAPI

# from orders.router import router as orders_router
from products.routers import router as products_router

app = FastAPI(title="Stealth startup homework")


@app.get("/")
def message_to_Borys():
    return {"Message to Borys": "Hello Borys, thank you for this opportunity!"}


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# app.include_router(orders_router)
app.include_router(products_router)


# @app.get("/authenticated-route")
# async def authenticated_route(user: User = Depends(current_active_user)):
#     return {"message": f"Hello {user.email}!"}
