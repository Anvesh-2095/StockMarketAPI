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
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)
    return {}