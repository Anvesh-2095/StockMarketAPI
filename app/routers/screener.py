from typing import List

from fastapi import APIRouter
from .. import models
from ..utils import filters
from ..database import cursor

router = APIRouter(
    prefix="/screener",
)

@router.get("/", response_model=List[models.FilteredStocksResponse])
def get_stocks(filters_json: dict, sort_by: str = None, sort_order: str = "asc", limit: int = 100, offset: int = 0):
    sql = filters.parse_query(filters_json)
    print(sql) # Debugging line to check the generated SQL query
    cursor.execute(sql)
    rows = cursor.fetchall()

    res: List[models.FilteredStocksResponse] = []
    for row in rows:
        stock = models.FilteredStocksResponse(
            name=row[0],
            short_code=row[1],
            industry=row[2],
            nse_price=row[3],
            bse_price=row[4],
        )
        res.append(stock)
    return res