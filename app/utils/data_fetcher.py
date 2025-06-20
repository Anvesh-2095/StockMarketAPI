from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
import httpx
from ..config import settings
from .. import models, database
from . import json_extractor

def fetch_and_store_data(name: str = "POLYCAB"):
    header = {
        "X-Api-Key": settings.API_KEY
    }
    response = httpx.get(f"https://stock.indianapi.in/stock?name={name}", headers=header)
    if response.status_code == 200:
        data = response.json()
        # print(f"Data fetched for {name} at {datetime.now(pytz.timezone('Asia/Kolkata'))}: {data}")
        stock: models.Stocks = json_extractor.extract_stock_from_json(data)
        # with database.connection.cursor() as cursor:
            # cursor.execute(
            #     """
            #     """
            # )
        # print(stock)
        with open (f"app/{name}.json", "w") as file:
            file.write(str(stock.model_dump_json()))
    else:
        print(f"Failed to fetch data for {name}. Status code: {response.status_code}")

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.add_job(
    fetch_and_store_data,
    trigger='cron',
    day_of_week='mon-fri',
    hour=15,
    minute=5, # 5 minutes after market close
)

scheduler.start()

if __name__ == "__main__":
    fetch_and_store_data()