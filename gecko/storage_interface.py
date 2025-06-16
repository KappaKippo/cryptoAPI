from sqlmodel import Session
from gecko.models import Coin


class StorageManager:
    def __init__(self, session: Session):
        self.session = session

    def commit_and_close(self):
        self.session.commit()
        self.session.close()

    def create_objects(self, coin: Coin):
        self.session.add(Coin(id=coin.id, symbol=coin.symbol, name=coin.name))
