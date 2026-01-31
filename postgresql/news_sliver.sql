CREATE SCHEMA IF NOT EXISTS sliver;

CREATE TABLE IF NOT EXISTS sliver.news_sliver (
    id SERIAL NOT NULL PRIMARY KEY,
    source_id TEXT,
    source_name TEXT,
    title TEXT NOT NULL,
    author TEXT,
    description TEXT,
    content TEXT,
    url TEXT NOT NULL,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);