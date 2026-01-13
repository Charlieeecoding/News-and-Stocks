CREATE SCHEMA IF NOT EXISTS bronze;
CREATE TABLE IF NOT EXISTS bronze.news_raw (
    id SERIAL PRIMARY KEY,
    source_id VARCHAR,
    source VARCHAR,
    title VARCHAR,
    author VARCHAR,
    description TEXT,
    url VARCHAR,
    urlToImage VARCHAR,
    publishedAt TIMESTAMP NOT NULL,
    raw_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);