from datetime import date
from typing import Optional, List

from .. import models

def get_value(financials: dict, statement: str, key: str) -> Optional[float]:
    for item in financials['stockFinancialMap'][statement]:
        if item['key'] == key:
            return float(item['value'])
    return None

def extract_shareholding(data: dict, target: str) -> List[models.ShareholdingEntry]:
    result: List[models.ShareholdingEntry] = []
    for group in data.get('shareholding', []):
        if group.get('displayName', '').lower() == target.lower():
            for entry in group.get('categories', []):
                try:
                    result.append(models.ShareholdingEntry(
                        date = date.fromisoformat(entry['holdingDate']),
                        percentage = float(entry['percentage'])
                    ))
                except Exception:
                    continue
    return result

def extract_stock_from_json(data: dict) -> models.Stocks:
    financials = data['financials']
    most_recent = financials[0]
    oldest = financials[-1] #TODO: check time passed from oldest, and fix all fields which use oldest data

    name: str = data['companyName']
    short_code: str = data['companyProfile']['exchangeCodeNse']
    industry: str = data['industry']
    nse_price: float = float(data['currentPrice']['NSE'])
    bse_price: float = float(data['currentPrice']['BSE'])

    short_name: str = name.replace(" Ltd", "")
    peer_match: dict = next(
        (p for p in data['companyProfile']['peerCompanyList'] if short_name in p['companyName']),
        {}
    )

    PERatio: float = peer_match.get('priceToEarningsValueRatio', 0.0)
    PBRatio: float = peer_match.get('priceToBookValueRatio', 0.0)
    debt_to_equity: float = peer_match.get('ltDebtPerEquityMostRecentFiscalYear', 0.0)
    market_cap: float = peer_match.get('marketCap', 0.0)
    _52_week_high: float = peer_match.get(data['yearHigh'])
    _52_week_low: float = peer_match.get(data['yearLow'])

    operating_income: float = get_value(most_recent, 'INC', 'OperatingIncome') or 0.0
    total_assets: float = get_value(most_recent, 'BAL', 'TotalAssets') or 0.0
    current_liabilities: float = get_value(most_recent, 'BAL', 'TotalCurrentLiabilities') or 0.0
    capital_employed: float = total_assets - current_liabilities
    ROCE: float = (operating_income / capital_employed) * 100 if capital_employed else 0.0

    rev_recent: float = get_value(most_recent, 'INC', 'Revenue') or 0.0
    rev_old: float = get_value(oldest, 'INC', 'Revenue') or 0.0
    revenue_growth: float = ((rev_recent - rev_old) / rev_old * 100) if rev_old else 0.0

    n_years: int = int(most_recent['FiscalYear']) - int(oldest['FiscalYear'])
    compounded_sales_growth: float = ((rev_recent / rev_old) ** (1 / n_years) - 1) * 100 if rev_old and n_years else 0.0

    np_recent: float = get_value(most_recent, 'INC', 'NetIncome') or 0.0
    np_old: float = get_value(oldest, 'INC', 'NetIncome') or 0.0
    compounded_profit_growth: float = ((np_recent / np_old) ** (1 / n_years) - 1) * 100 if np_old and n_years else 0.0

    EPS_recent: float = get_value(most_recent, 'INC', 'DilutedEPSExcludingExtraOrdItems') or 0.0
    EPS_old: float = get_value(oldest, 'INC', 'DilutedEPSExcludingExtraOrdItems') or 0.0
    EPS_growth: float = ((EPS_recent / EPS_old) ** (1 / n_years) - 1) * 100 if EPS_old and n_years else 0.0


    borrow: float = get_value(most_recent, 'BAL', 'TotalDebt') or 0.0

    ROE: float = peer_match.get('returnOnAverageEquityTrailing12Month', 0.0)

    shareholding_pattern_promoter: List[models.ShareholdingEntry] = extract_shareholding(data, "Promoters")
    shareholding_pattern_fii: List[models.ShareholdingEntry] = extract_shareholding(data, "FII")
    shareholding_pattern_mf: List[models.ShareholdingEntry] = extract_shareholding(data, "MF")
    shareholding_pattern_others: List[models.ShareholdingEntry] = extract_shareholding(data, "Others")

    return models.Stocks(
        name=name,
        short_code=short_code,
        industry=industry,
        nse_price=nse_price,
        bse_price=bse_price,
        PERatio=PERatio,
        PBRatio=PBRatio,
        debt_to_equity=debt_to_equity,
        ROCE=ROCE,
        ROE=ROE,
        market_cap=market_cap,
        _52_week_high=_52_week_high,
        _52_week_low=_52_week_low,
        compounded_sales_growth=compounded_sales_growth,
        compounded_profit_growth=compounded_profit_growth,
        shareholding_pattern_promoter=shareholding_pattern_promoter,
        shareholding_pattern_fii=shareholding_pattern_fii,
        shareholding_pattern_mf=shareholding_pattern_mf,
        shareholding_pattern_others=shareholding_pattern_others,
        revenue=rev_recent,
        revenue_growth=revenue_growth,
        borrow=borrow,
        EPS_growth=EPS_growth,
        EPS=EPS_recent,
        net_profit=np_recent
    )