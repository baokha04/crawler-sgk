from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domains.orders.models import Order
from app.domains.orders.schemas import OrderCreate, OrderUpdate

class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: int) -> Order | None:
        result = await self.db.execute(select(Order).filter(Order.id == id))
        return result.scalars().first()

    async def get_multi(self, skip: int = 0, limit: int = 100) -> list[Order]:
        result = await self.db.execute(select(Order).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, obj_in: OrderCreate) -> Order:
        db_obj = Order(
            product_name=obj_in.product_name,
            quantity=obj_in.quantity,
            price=obj_in.price
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: Order, obj_in: OrderUpdate) -> Order:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def remove(self, id: int) -> Order | None:
        db_obj = await self.get(id)
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.commit()
        return db_obj
