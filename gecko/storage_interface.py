from gecko.models import Coin
from sqlmodel import select


class StorageManager:
    def __init__(self, session):
        self.session = session

    def commit_and_close(self):
        self.session.commit()
        self.session.close()

    def create_objects(self, coin: Coin):
        self.session.add(Coin(gecko_id=coin.id, symbol=coin.symbol, name=coin.name))

    def get_objects(self, field, values: list):
        query = select(Coin.id).where(field.in_(values))
        results = self.session.exec(query)
        return [result for result in results]
