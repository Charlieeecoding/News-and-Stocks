CREATE SCHEMA IF NOT EXISTS bronze;

CREATE TABLE IF NOT EXISTS bronze.stock_prices_bronze (
    id SERIAL NOT NULL PRIMARY KEY,
    symbol TEXT NOT NULL,
    Datetime_hkt TIMESTAMP NOT NULL,
    Open FLOAT,
    High FLOAT,
    Low FLOAT,
    Close FLOAT,
    Volume BIGINT,
    Dividends FLOAT,
    Stock_Spilits FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);