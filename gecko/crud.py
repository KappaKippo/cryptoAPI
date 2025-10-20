from sqlmodel import Session

from gecko.models import Coin


def create_or_update(session: Session, data: list[Coin]):
    for coin in data:
        session.add(coin)
        print(f"Coin {coin.name} added to DB.")

    session.commit()
    print("Changes committed to DB.")
