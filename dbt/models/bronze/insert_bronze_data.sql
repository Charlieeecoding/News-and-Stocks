INSERT INTO bronze.news_raw (
    id,
    source_id,
    source,
    title,
    author,
    description,
    url,
    urlToImage,
    publishedAt,
    raw_data JSONB,
    created_at
    )
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW());