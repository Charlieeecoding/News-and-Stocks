CREATE SCHEMA IF NOT EXISTS bronze;

CREATE TABLE IF NOT EXISTS bronze.stock_prices_bronze (
    time TIMESTAMP NOT NULL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT,
    fetch_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    vwap FLOAT, 
    transacrtions BIGINT
);