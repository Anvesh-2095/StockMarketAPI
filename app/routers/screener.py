from typing import List

from fastapi import APIRouter
from .. import models

router = APIRouter(
    prefix="/screener",
)

@router.get("/", response_model=List[models.FilteredStocksResponse])
def get_stocks(filters: dict, sort_by: str = None, sort_order: str = "asc", limit: int = 100, offset: int = 0):
    pass