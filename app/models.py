import json
from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from dataclasses import dataclass

class ShareholdingEntry(BaseModel):
    date: date
    percentage: float

@dataclass
class Stocks(BaseModel):
    name: str
    short_code: str
    industry: str
    nse_price: float
    bse_price: float
    PERatio: float
    PBRatio: float
    debt_to_equity: float
    ROCE: float
    ROE: float
    market_cap: float
    _52_week_high: float
    _52_week_low: float
    compounded_sales_growth: float
    compounded_profit_growth: float
    shareholding_pattern_promoter: List[ShareholdingEntry]
    shareholding_pattern_fii: List[ShareholdingEntry]
    shareholding_pattern_mf: List[ShareholdingEntry]
    shareholding_pattern_others: List[ShareholdingEntry]
    revenue: float
    revenue_growth: float
    borrow: float
    EPS_growth: float
    EPS: float
    net_profit: float

class StocksResponse(Stocks):
    pass

class FilteredStocksResponse(BaseModel):
    name: str
    short_code: str
    industry: str
    nse_price: float
    bse_price: float