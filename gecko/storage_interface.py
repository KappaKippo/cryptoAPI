import datetime

from gecko.models import Coin, Price
from sqlmodel import select


class StorageManager:
    def __init__(self, session):
        self.session = session

    async def commit_and_close(self):
        self.session.commit()
        self.session.close()

    async def create_coins(self, coin: Coin):
        self.session.add(Coin(gecko_id=coin.id, symbol=coin.symbol, name=coin.name))

    async def create_and_correlate_price(
        self, coin_ids: list[int], prices: list[float]
    ):
        [
            self.session.add(
                Price(
                    price=price,
                    created=datetime.datetime.now(),
                    coin_id=coin_ids[index],
                )
            )
            for index, price in enumerate(prices)
        ]
        await self.commit_and_close()

    async def get_objects(self, field, values: list) -> list:
        query = select(Coin.id).where(field.in_(values))
        results = self.session.exec(query)
        return [result for result in results]
