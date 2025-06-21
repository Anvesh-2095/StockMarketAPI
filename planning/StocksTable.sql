-- This SQL script creates a database schema for managing stock data, including stock details and shareholding information.
CREATE TABLE IF NOT EXISTS stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    short_code VARCHAR(50) NOT NULL,
    industry VARCHAR(255),
    nse_price FLOAT,
    bse_price FLOAT,
    PERatio FLOAT,
    PBRatio FLOAT,
    debt_to_equity FLOAT,
    ROCE FLOAT,
    ROE FLOAT,
    market_cap FLOAT,
    _52_week_high FLOAT,
    _52_week_low FLOAT,
    compounded_sales_growth FLOAT,
    compounded_profit_growth FLOAT,
    revenue FLOAT,
    revenue_growth FLOAT,
    borrow FLOAT,
    EPS_growth FLOAT,
    EPS FLOAT,
    net_profit FLOAT,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shareholding_promoter (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT,
    report_date DATE,
    percentage FLOAT,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shareholding_fii (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT,
    report_date DATE,
    percentage FLOAT,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shareholding_mf (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT,
    report_date DATE,
    percentage FLOAT,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shareholding_others (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT,
    report_date DATE,
    percentage FLOAT,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shares_to_fetch (
    name VARCHAR(255) PRIMARY KEY
);