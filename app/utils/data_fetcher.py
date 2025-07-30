from typing import List

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
import httpx

from app.models import ShareholdingEntry
from ..config import settings
from .. import models, database
from ..database import conn, cursor
from . import raw_json_to_object

# TODO: Add error handling and logging
# TODO: Add a way to fetch multiple stocks at once to optimize performance

def generate_shareholding_inserts(stock_id: int, pattern: List[ShareholdingEntry], table: str) -> List[tuple[str, dict]]:
    sql = f"""
        INSERT INTO {table} (stock_id, report_date, percentage, recorded_at)
        VALUES (%(stock_id)s, %(report_date)s, %(percentage)s, NOW());
    """
    queries = []
    for entry in pattern:
        queries.append((sql, {
            "stock_id": stock_id,
            "report_date": entry.date,
            "percentage": entry.percentage
        }))
    return queries


def fetch_and_store_data(name: str = "POLYCAB"):
    header = {
        "X-Api-Key": settings.API_KEY
    }

    sql = """SELECT * FROM stocks WHERE name = %s or short_code = %s and DATE(recorded_at) = DATE(NOW())"""
    cursor.execute(sql, (name, name))
    existing_stock = cursor.fetchone()
    if existing_stock:
        print(f"Data for {name} already exists in the database. Skipping fetch.")
        return

    response = httpx.get(f"https://stock.indianapi.in/stock?name={name}", headers=header)
    if response.status_code == 200:
        data = response.json()
        # print(f"Data fetched for {name} at {datetime.now(pytz.timezone('Asia/Kolkata'))}: {data}")
        stock: models.Stocks = raw_json_to_object.extract_stock_from_json(data)

        sql = """
        INSERT INTO stocks ( 
        name, short_code, industry, nse_price, bse_price,
        PERatio, PBRatio, debt_to_equity, ROCE, ROE, market_cap, _52_week_high, _52_week_low,
        compounded_sales_growth, compounded_profit_growth, revenue, revenue_growth, borrow,
        EPS_growth, EPS, net_profit, recorded_at
        )
        VALUES (
        %(name)s, %(short_code)s, %(industry)s, %(nse_price)s, %(bse_price)s, 
        %(PERatio)s, %(PBRatio)s, %(debt_to_equity)s, %(ROCE)s, %(ROE)s, %(market_cap)s, %(_52_week_high)s, %(_52_week_low)s,
        %(compounded_sales_growth)s, %(compounded_profit_growth)s, %(revenue)s, %(revenue_growth)s, %(borrow)s, 
        %(EPS_growth)s, %(EPS)s, %(net_profit)s, NOW()
        );
        """

        values = {
            "name": stock.name,
            "short_code": stock.short_code,
            "industry": stock.industry,
            "nse_price": stock.nse_price,
            "bse_price": stock.bse_price,
            "PERatio": stock.PERatio,
            "PBRatio": stock.PBRatio,
            "debt_to_equity": stock.debt_to_equity,
            "ROCE": stock.ROCE,
            "ROE": stock.ROE,
            "market_cap": stock.market_cap,
            "_52_week_high": stock.prev_52_week_high,
            "_52_week_low": stock.prev_52_week_low,
            "compounded_sales_growth": stock.compounded_sales_growth,
            "compounded_profit_growth": stock.compounded_profit_growth,
            "revenue": stock.revenue,
            "revenue_growth": stock.revenue_growth,
            "borrow": stock.borrow,
            "EPS_growth": stock.EPS_growth,
            "EPS": stock.EPS,
            "net_profit": stock.net_profit
        }

        cursor.execute(sql, values)
        conn.commit()

        stock_id = cursor.lastrowid # use of returning keyword is not supported by many mysql-connector-python

        promoter_queries = generate_shareholding_inserts(stock_id, stock.shareholding_pattern_promoter,
                                                         'shareholding_promoter')
        fii_queries = generate_shareholding_inserts(stock_id, stock.shareholding_pattern_fii, 'shareholding_fii')
        mf_queries = generate_shareholding_inserts(stock_id, stock.shareholding_pattern_mf, 'shareholding_mf')
        others_queries = generate_shareholding_inserts(stock_id, stock.shareholding_pattern_others,
                                                       'shareholding_others')

        for query, params in promoter_queries + fii_queries + mf_queries + others_queries:
            cursor.execute(query, params)
        conn.commit()

        # with open (f"app/{name}.json", "w") as file:
        #     file.write(str(stock.model_dump_json()))
    else:
        print(f"Failed to fetch data for {name}. Status code: {response.status_code}")

def fetch_and_store_data_all(): # TODO: add batch inserts later
    """
    Fetches data for all stocks and stores it in the database.
    This function is intended to be run once a day at market close.
    """
    cursor.execute('SELECT * FROM shares_to_fetch')
    stock_names = [row[0] for row in cursor.fetchall()]
    for name in stock_names:
        fetch_and_store_data(name)
        # print(f"Data fetched and stored for {name} at {datetime.now(pytz.timezone('Asia/Kolkata'))}")


scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.add_job(
    fetch_and_store_data_all,
    trigger='cron',
    day_of_week='mon-fri',
    hour=15,
    minute=5, # 5 minutes after market close
)

scheduler.start()

if __name__ == "__main__":
    fetch_and_store_data_all()