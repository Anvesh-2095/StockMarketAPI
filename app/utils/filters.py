def parse_query(features: dict) -> str:
    """
    Returns a SQL query string based on the provided features dictionary.
    This function has been revised with a more robust query to correctly
    identify the single latest record for each stock before filtering.

    IMPORTANT SECURITY WARNING: This function remains vulnerable to SQL injection.
    For a production application, you MUST use parameterized queries provided
    by your database driver to prevent security risks.

    :param features: Dictionary containing feature names and their values.
    :return: A complete SQL query string.
    """
    # TODO: fix the SQL injection vulnerability by using parameterized queries
    # This multi-step query is more robust. It first finds the latest shareholding
    # report date for each stock, then LEFT JOINs all data to that date. This
    # prevents stocks from being dropped if some shareholding data is missing.
    base_query = """
    WITH LatestShareholdingDate AS (
        -- Step 1: Find the most recent report_date for each stock_id.
        -- We assume 'shareholding_promoter' is a reliable source for the latest date.
        SELECT
            stock_id,
            MAX(report_date) as latest_report_date
        FROM shareholding_promoter
        GROUP BY stock_id
    ),
    RankedStockData AS (
        -- Step 2: Join all data using the latest_report_date and rank the results.
        SELECT
            s.name,
            s.short_code,
            s.industry,
            s.nse_price,
            s.bse_price,
            s.PERatio,
            s.PBRatio,
            s.debt_to_equity,
            s.ROCE,
            s.ROE,
            s.market_cap,
            s._52_week_high,
            s._52_week_low,
            s.compounded_sales_growth,
            s.compounded_profit_growth,
            s.revenue,
            s.revenue_growth,
            s.borrow,
            s.EPS_growth,
            s.EPS,
            s.net_profit,
            pro.percentage AS promoter_shareholding_percentage,
            fii.percentage AS fii_shareholding_percentage,
            mf.percentage AS mf_shareholding_percentage,
            oth.percentage AS other_shareholding_percentage,
            -- Rank entries for each stock by the stock's recorded_at timestamp.
            -- This ensures we get the very latest stock price for the latest reporting period.
            ROW_NUMBER() OVER(PARTITION BY s.short_code ORDER BY s.recorded_at DESC) as rn
        FROM
            stocks AS s
        -- Use LEFT JOINs so that a stock isn't excluded if any data is missing.
        LEFT JOIN LatestShareholdingDate lsd ON s.id = lsd.stock_id
        LEFT JOIN shareholding_promoter pro ON s.id = pro.stock_id AND pro.report_date = lsd.latest_report_date
        LEFT JOIN shareholding_fii fii ON s.id = fii.stock_id AND fii.report_date = lsd.latest_report_date
        LEFT JOIN shareholding_mf mf ON s.id = mf.stock_id AND mf.report_date = lsd.latest_report_date
        LEFT JOIN shareholding_others oth ON s.id = oth.stock_id AND oth.report_date = lsd.latest_report_date
    )
    -- Step 3: Select all columns for the top-ranked record for each stock.
    SELECT
        *
    FROM
        RankedStockData
    WHERE
        rn = 1
    """

    filters = []
    # This helper function quotes string values to prevent SQL syntax errors.
    def quote_if_string(val):
        if isinstance(val, str):
            # Basic escape for single quotes within the string value
            escaped_val = val.replace("'", "''")
            return f"'{escaped_val}'"
        return val

    # The for loop runs to completion, building the full list of filters.
    for key, value in features.items():
        # The column name is derived by removing the suffix from the key.
        if key.endswith("_low"):
            column = key[:-4]
            filters.append(f"{column} > {value}")
        elif key.endswith("_high"):
            column = key[:-5]
            filters.append(f"{column} < {value}")
        elif key.endswith("_lowequal"):
            column = key[:-9]
            filters.append(f"{column} >= {value}")
        elif key.endswith("_highequal"):
            column = key[:-10]
            filters.append(f"{column} <= {value}")
        elif key.endswith("_equal"):
            column = key[:-6]
            filters.append(f"{column} = {quote_if_string(value)}")
        elif key.endswith("_not"):
            column = key[:-4]
            filters.append(f"{column} != {quote_if_string(value)}")
        elif key.endswith("_like"):
            column = key[:-5]
            filters.append(f"{column} LIKE '%{str(value).replace("'", "''")}%'")
        elif key.endswith("_between"):
            column = key[:-8]
            if isinstance(value, (list, tuple)) and len(value) == 2:
                filters.append(f"{column} BETWEEN {value[0]} AND {value[1]}")

    # This block is now OUTSIDE the for loop.
    # It runs only after the loop has finished.
    if filters:
        # Each condition is appended with AND.
        # We need to wrap the base query to apply the WHERE clause correctly.
        query_with_filters = f"SELECT * FROM ({base_query}) AS final_data WHERE " + " AND ".join(filters)
        return query_with_filters

    # This will only be reached if the 'features' dictionary was empty.
    # We need to wrap the base query here as well for consistency.
    return f"SELECT * FROM ({base_query}) AS final_data"
