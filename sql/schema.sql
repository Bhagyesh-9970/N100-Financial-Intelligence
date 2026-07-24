PRAGMA foreign_keys = ON;

-- =====================================================
-- COMPANIES
-- =====================================================

CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY,
    company_id TEXT UNIQUE NOT NULL,
    company_name TEXT,
    isin TEXT,
    sector TEXT,
    broad_sector TEXT,
    industry TEXT
);


-- =====================================================
-- PROFIT AND LOSS
-- =====================================================

CREATE TABLE IF NOT EXISTS profitandloss (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    year TEXT,

    sales REAL,
    expenses REAL,
    operating_profit REAL,
    opm_percentage REAL,
    other_income REAL,
    interest REAL,
    depreciation REAL,
    profit_before_tax REAL,
    tax_percentage REAL,
    net_profit REAL,
    eps REAL,
    dividend_payout REAL,

    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);


-- =====================================================
-- BALANCE SHEET
-- =====================================================

CREATE TABLE IF NOT EXISTS balancesheet (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    year TEXT,

    equity_capital REAL,
    reserves REAL,
    borrowings REAL,
    other_liabilities REAL,
    total_liabilities REAL,
    fixed_assets REAL,
    cwip REAL,
    investments REAL,
    other_asset REAL,
    total_assets REAL,

    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);


-- =====================================================
-- CASH FLOW
-- =====================================================

CREATE TABLE IF NOT EXISTS cashflow (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    year TEXT,

    operating_activity REAL,
    investing_activity REAL,
    financing_activity REAL,
    net_cash_flow REAL,

    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);


-- =====================================================
-- FINANCIAL RATIOS
-- =====================================================

CREATE TABLE IF NOT EXISTS financial_ratios (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    year TEXT,

    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct REAL,
    debt_to_equity REAL,
    interest_coverage REAL,
    asset_turnover REAL,
    free_cash_flow_cr REAL,
    capex_cr REAL,
    earnings_per_share REAL,
    book_value_per_share REAL,
    dividend_payout_ratio_pct REAL,
    total_debt_cr REAL,
    cash_from_operations_cr REAL,

    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);


-- =====================================================
-- DOCUMENTS
-- =====================================================

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    document_type TEXT,
    document_name TEXT,
    document_url TEXT,

    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);


-- =====================================================
-- ANALYSIS
-- =====================================================

CREATE TABLE IF NOT EXISTS analysis (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    analysis TEXT,

    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);


-- =====================================================
-- PROS AND CONS
-- =====================================================

CREATE TABLE IF NOT EXISTS prosandcons (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    pros TEXT,
    cons TEXT,

    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);


-- =====================================================
-- MARKET CAP
-- =====================================================

CREATE TABLE IF NOT EXISTS market_cap (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,
    market_cap_cr REAL,

    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);


-- =====================================================
-- PEER GROUPS
-- =====================================================

CREATE TABLE IF NOT EXISTS peer_groups (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    peer_group_name TEXT,

    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);


-- =====================================================
-- SECTORS
-- =====================================================

CREATE TABLE IF NOT EXISTS sectors (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    sector TEXT,
    broad_sector TEXT,
    industry TEXT,

    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);


-- =====================================================
-- STOCK PRICES
-- =====================================================

CREATE TABLE IF NOT EXISTS stock_prices (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,

    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);