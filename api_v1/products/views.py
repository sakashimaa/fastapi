from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from .dependencies import product_by_id

router = APIRouter(tags=["products"])


@router.get("/", response_model=list[Product])
async def get_products(
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency,
    )
):
    products = await crud.get_products(session=session)
    return products


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product: ProductCreate,
    session: AsyncSession = Depends(
        db_helper.session_dependency,
    ),
):
    return await crud.create_product(product=product, session=session)


@router.get("/{product_id}/", response_model=Product)
async def get_product(product: Product = Depends(product_by_id)) -> Product:
    return product


@router.put("/{product_id}/")
async def update_product(
    product_update: ProductUpdate,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(
        db_helper.session_dependency,
    ),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.patch("/{product_id}/")
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(
        db_helper.session_dependency,
    ),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
    )


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(
        db_helper.session_dependency,
    ),
) -> None:
    await crud.delete_product(
        session=session,
        product=product,
    )
