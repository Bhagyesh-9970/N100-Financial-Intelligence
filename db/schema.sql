PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS companies (

    company_id INTEGER PRIMARY KEY,

    ticker TEXT UNIQUE NOT NULL,

    company_name TEXT NOT NULL,

    sector TEXT,

    industry TEXT,

    isin TEXT,

    listing_date TEXT

);
CREATE TABLE IF NOT EXISTS profitandloss (

    company_id INTEGER,

    year INTEGER,

    sales REAL,

    operating_profit REAL,

    opm REAL,

    net_profit REAL,

    eps REAL,

    tax_rate REAL,

    PRIMARY KEY(company_id, year),

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

);
CREATE TABLE IF NOT EXISTS balancesheet (

    company_id INTEGER,

    year INTEGER,

    total_assets REAL,

    total_liabilities REAL,

    total_equity REAL,

    PRIMARY KEY(company_id, year),

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

);
CREATE TABLE IF NOT EXISTS cashflow (

    company_id INTEGER,

    year INTEGER,

    cash_from_operating_activity REAL,

    cash_from_investing_activity REAL,

    cash_from_financing_activity REAL,

    net_cash_flow REAL,

    PRIMARY KEY(company_id, year),

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

);
CREATE TABLE IF NOT EXISTS analysis (

    company_id INTEGER,
    year INTEGER,

    market_cap REAL,
    current_price REAL,
    high_low TEXT,
    stock_pe REAL,
    book_value REAL,
    dividend_yield REAL,
    roce REAL,
    roe REAL,

    PRIMARY KEY(company_id, year),

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

);
CREATE TABLE IF NOT EXISTS documents (

    document_id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER,

    annual_report TEXT,
    concall_pdf TEXT,
    investor_presentation TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

);
CREATE TABLE IF NOT EXISTS prosandcons (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER,

    pros TEXT,
    cons TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

);
CREATE TABLE IF NOT EXISTS sectors (

    sector_id INTEGER PRIMARY KEY AUTOINCREMENT,

    sector_name TEXT UNIQUE

);
CREATE TABLE IF NOT EXISTS stock_prices (

    company_id INTEGER,

    trade_date TEXT,

    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume INTEGER,

    PRIMARY KEY(company_id, trade_date),

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

);
CREATE TABLE IF NOT EXISTS financial_ratios (

    company_id INTEGER,

    year INTEGER,

    pe REAL,
    pb REAL,
    eps REAL,
    roce REAL,
    roe REAL,
    debt_to_equity REAL,
    current_ratio REAL,

    PRIMARY KEY(company_id, year),

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

);
CREATE TABLE IF NOT EXISTS peer_groups (

    peer_id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER,

    peer_company TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)

);

COMMIT;
