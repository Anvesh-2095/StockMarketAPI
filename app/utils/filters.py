def parse_query(features : dict) -> str:
    """
    returns a sql query string based on the provided features dictionary.
    features dict is extracted from the request body json on route /screener
    :param features: Dictionary containing feature names and their values.
    :return: SQL query string.
    """
    # SQL Query for constructing a table with all features from stocks and percentages from shareholding tables
    table = """
    SELECT distinct(s.name), s.short_code, s.industry, s.nse_price, s.bse_price, 
    s.PERatio, s.PBRatio, s.debt_to_equity, s.ROCE, s.ROE, s.market_cap, 
    s._52_week_high, s._52_week_low, s.compounded_sales_growth, s.compounded_profit_growth, 
    s.revenue, s.revenue_growth, s.borrow, s.EPS_growth, s.EPS, s.net_profit, 
    pro.percentage AS promoter_shareholding_percentage,
    fii.percentage AS fii_shareholding_percentage,
    mf.percentage AS mf_shareholding_percentage,
    oth.percentage AS other_shareholding_percentage,
    s.recorded_at, pro.report_date
    FROM stocks AS s, shareholding_promoter AS pro,shareholding_fii as fii,
    shareholding_mf as mf, shareholding_others as oth
    WHERE s.id = pro.stock_id AND s.id = fii.stock_id AND s.id = mf.stock_id AND s.id = oth.stock_id
    AND pro.report_date = fii.report_date AND pro.report_date = mf.report_date AND pro.report_date = oth.report_date
    AND DATE(s.recorded_at) = DATE(pro.recorded_at) AND DATE(s.recorded_at) = DATE(oth.recorded_at)
    AND DATE(s.recorded_at) = DATE(fii.recorded_at) AND DATE(s.recorded_at) = DATE(mf.recorded_at)
    ORDER BY s.recorded_at DESC, pro.report_date DESC
    """
    res = f"SELECT DISTINCT name, short_code FROM ({table}) WHERE TRUE "

    for key, value in features.items():
        if key.endswith("_low"):
            res += f"AND {key[:-4]} > {value}"
        elif key.endswith("_high"):
            res += f"AND {key[:-5]} < {value}"
        elif key.endswith("_lowequal"):
            res += f"AND {key[:-9]} >= {value}"
        elif key.endswith("_highequal"):
            res += f"AND {key[:-10]} <= {value}"
        elif key.endswith("_equal"):
            res += f"AND {key[:-6]} = {value}"
        elif key.endswith("_not"):
            res += f"AND {key[:-4]} != {value}"
        elif key.endswith("_like"):
            res += f"AND {key[:-5]} LIKE '%{value}%'"
        elif key.endswith("_between'"):
            res += f"AND {key[:-8]} BETWEEN {value[0]} AND {value[1]}"

    return res