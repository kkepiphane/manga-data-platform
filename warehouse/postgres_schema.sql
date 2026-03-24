CREATE TABLE IF NOT EXISTS mangas (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    title_clean TEXT,
    source TEXT,
    url TEXT,
    scraped_at TIMESTAMP,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_manga UNIQUE (title, url) -- Évite les doublons
);
