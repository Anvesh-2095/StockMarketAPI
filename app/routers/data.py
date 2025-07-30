from datetime import datetime
from .. import models
from fastapi import APIRouter, HTTPException
# from ..database import conn, cursor
from ..utils import sql_to_object

router = APIRouter(
    prefix="/data",
    tags=["data"],
)

# TODO: make sql strings more secure against SQL injection

@router.get("/{name}", response_model=models.StocksResponse)
def get_latest_data(name: str):
    sql = f"""
    SELECT * FROM stocks WHERE name = '{name}' OR short_code = '{name}' ORDER BY recorded_at DESC LIMIT 1;
    """
    stock: models.Stocks = sql_to_object.get_one_obj(sql)
    # print(stock.model_dump())
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return models.StocksResponse(**stock.model_dump())

@router.get("/{name}/{date}", response_model=models.StocksResponse)
def get_data_by_date(name: str, date: datetime):
    sql = f"""
    SELECT * FROM stocks WHERE (name = '{name}' OR short_code = '{name}') AND DATE(recorded_at) = '{date.date()}' ORDER BY recorded_at DESC LIMIT 1;
    """
    stock: models.Stocks = sql_to_object.get_one_obj(sql)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return models.StocksResponse(**stock.model_dump())