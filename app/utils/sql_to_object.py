from typing import List

from .. import models
from ..database import conn, cursor

def get_shareholding_data(stock_id: int, table: str) -> List[models.ShareholdingEntry]:
    """
    Fetch shareholding data for a given stock ID from the specified table.

    Args:
        stock_id (int): The ID of the stock.
        table (str): The name of the table to fetch data from.

    Returns:
        List[models.ShareholdingEntry]: List of ShareholdingEntry objects populated with data from the database.
    """
    cursor.execute(f"SELECT * FROM {table} WHERE stock_id = %s", (stock_id,))
    rows = cursor.fetchall()

    return [
        models.ShareholdingEntry(
            date=row[1],
            percentage=row[2]
        ) for row in rows
    ] if rows else []


def get_one_obj(sql: str) -> models.Stocks:
    """
    Convert SQL query result to Stocks object.

    Args:
        sql (str): SQL query string. - with or without filters

    Returns:
        models.Stocks: Stocks object populated with data from the SQL query.
    """
    cursor.execute(sql)
    row = cursor.fetchone()

    if not row:
        return None

    stock_id: int = row[0]

    promoter_shareholding = get_shareholding_data(stock_id, "shareholding_promoter")
    fii_shareholding = get_shareholding_data(stock_id, "shareholding_fii")
    mf_shareholding = get_shareholding_data(stock_id, "shareholding_mf")
    other_shareholding = get_shareholding_data(stock_id, "shareholding_others")

    return models.Stocks(
        name=row[1],
        short_code=row[2],
        industry=row[3],
        nse_price=row[4],
        bse_price=row[5],
        PERatio=row[6],
        PBRatio=row[7],
        debt_to_equity=row[8],
        ROCE=row[9],
        ROE=row[10],
        market_cap=row[11],
        prev_52_week_high=row[12],
        prev_52_week_low=row[13],
        compounded_sales_growth=row[14],
        compounded_profit_growth=row[15],
        revenue=row[16],
        revenue_growth=row[17],
        borrow=row[18],
        EPS_growth=row[19],
        EPS=row[20],
        net_profit=row[21],
        shareholding_pattern_promoter=promoter_shareholding,
        shareholding_pattern_fii=fii_shareholding,
        shareholding_pattern_mf=mf_shareholding,
        shareholding_pattern_others=other_shareholding
    )

def get_all_objs(sql: str) -> List[models.Stocks]:
    """
    Convert SQL query result to a list of Stocks objects.

    Args:
        sql (str): SQL query string. - with or without filters

    Returns:
        List[models.Stocks]: List of Stocks objects populated with data from the SQL query.
    """
    cursor.execute(sql)
    rows = cursor.fetchall()

    if not rows:
        return []

    stocks = []
    for row in rows:
        stock_id: int = row[0]

        promoter_shareholding = get_shareholding_data(stock_id, "shareholding_promoter")
        fii_shareholding = get_shareholding_data(stock_id, "shareholding_fii")
        mf_shareholding = get_shareholding_data(stock_id, "shareholding_mf")
        other_shareholding = get_shareholding_data(stock_id, "shareholding_others")

        stocks.append(models.Stocks(
            name=row[1],
            short_code=row[2],
            industry=row[3],
            nse_price=row[4],
            bse_price=row[5],
            PERatio=row[6],
            PBRatio=row[7],
            debt_to_equity=row[8],
            ROCE=row[9],
            ROE=row[10],
            market_cap=row[11],
            prev_52_week_high=row[12],
            prev_52_week_low=row[13],
            compounded_sales_growth=row[14],
            compounded_profit_growth=row[15],
            revenue=row[16],
            revenue_growth=row[17],
            borrow=row[18],
            EPS_growth=row[19],
            EPS=row[20],
            net_profit=row[21],
            shareholding_pattern_promoter=promoter_shareholding,
            shareholding_pattern_fii=fii_shareholding,
            shareholding_pattern_mf=mf_shareholding,
            shareholding_pattern_others=other_shareholding
        ))