from datetime import datetime
from .. import models
from fastapi import APIRouter

router = APIRouter(
    prefix="/data",
)

@router.get("/{name}", response_model=models.StocksResponse)
def get_latest_data(name: str):
    pass

@router.get("/{name}/{date}", response_model=models.StocksResponse)
def get_data_by_date(name: str, date: datetime):
    pass