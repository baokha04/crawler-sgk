from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.domains.orders.schemas import Order, OrderCreate, OrderUpdate
from app.domains.orders.services import OrderService

router = APIRouter()

@router.get("/", response_model=list[Order])
async def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    return await service.get_orders(skip=skip, limit=limit)

@router.post("/", response_model=Order)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    return await service.create_order(order_in)

@router.get("/{order_id}", response_model=Order)
async def read_order(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    order = await service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=Order)
async def update_order(
    order_id: int,
    order_in: OrderUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    order = await service.update_order(order_id, order_in)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.delete("/{order_id}", response_model=Order)
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = OrderService(db)
    order = await service.delete_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
