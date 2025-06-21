from fastapi import Query, HTTPException, status
from typing import Annotated
from gecko.models import Coin


def get_and_validate_ids_names_symbols_params(
    ids: Annotated[str, Query()] = None,
    names: Annotated[str, Query()] = None,
    symbols: Annotated[str, Query()] = None,
):
    if not ids and not names and not symbols:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="One of ids/names/symbols parameter should be given",
        )

    values = {"ids": ids, "names": names, "symbols": symbols}

    if ids:
        values.update({"correlated_field": Coin.gecko_id, "values": ids.split(",")})
        return values
    elif names:
        values.update({"correlated_field": Coin.name, "values": names.split(",")})
        return values
    else:
        values.update({"correlated_field": Coin.symbol, "values": symbols.split(",")})
        return values
