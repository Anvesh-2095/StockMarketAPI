class Stocks:
    name: str
    short_code: str
    industry: str
    nse_price: float
    bse_price: float
    PERatio: float
    PBRatio: float
    debt_to_equity: float
    ROCE : float
    ROE: float
    market_cap: float
    _52_week_high: float
    _52_week_low: float
    compounded_sales_growth : float # there may be multiple occurrences, one each for current year, previous 12 months and last 5 years
    compounded_profit_growth: float # there may be multiple occurrences, one each for current year, previous 12 months and last 5 years
    shareholding_pattern_promoter: list[4]
    shareholding_pattern_fii: list[4]
    shareholding_pattern_mf: list[4]
    shareholding_pattern_others: list[4]
    revenue: float
    revenue_growth: float
    borrow: float
    EPS_growth: float
    EPS: float
    net_profit : float