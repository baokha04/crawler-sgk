from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.orders.repository import OrderRepository
from app.domains.orders.schemas import OrderCreate, OrderUpdate
from app.domains.orders.models import Order

class OrderService:
    def __init__(self, db: AsyncSession):
        self.repository = OrderRepository(db)

    async def get_order(self, order_id: int) -> Order | None:
        return await self.repository.get(order_id)

    async def get_orders(self, skip: int = 0, limit: int = 100) -> list[Order]:
        return await self.repository.get_multi(skip=skip, limit=limit)

    async def create_order(self, order_in: OrderCreate) -> Order:
        # Business logic can go here
        return await self.repository.create(order_in)

    async def update_order(self, order_id: int, order_in: OrderUpdate) -> Order | None:
        db_obj = await self.repository.get(order_id)
        if not db_obj:
            return None
        return await self.repository.update(db_obj, order_in)

    async def delete_order(self, order_id: int) -> Order | None:
        return await self.repository.remove(order_id)
