-- SQLite Harvest Domain Staging Schema (staging_harvest.sql)
-- Domain 1: Raw Ingestion & Outpost Sweeps (Mythos, AI, OSS)
-- Architectural Rule: Pure text ingestion only. Decoupled from Bear Mode (vectors/Gua) and Mianzi (attribution/publish).

CREATE TABLE IF NOT EXISTS harvest_runs (
    run_id TEXT PRIMARY KEY,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    targets_scraped INTEGER DEFAULT 0,
    candidates_ingested INTEGER DEFAULT 0,
    run_status TEXT NOT NULL CHECK (run_status IN ('running', 'completed', 'failed', 'partial'))
);

CREATE TABLE IF NOT EXISTS harvest_candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_uid TEXT UNIQUE NOT NULL,           -- Unique hash or permalink slug key
    domain_category TEXT NOT NULL CHECK (domain_category IN ('mythos', 'ai_mechanics', 'oss_tooling')),
    source_platform TEXT NOT NULL,             -- e.g. 'reddit', 'arxiv', 'github', 'rss', 'huggingface'
    credit_uri TEXT NOT NULL,                  -- External source URL / permalink
    title TEXT NOT NULL,                       -- Raw title / headline
    raw_body TEXT,                             -- Text abstract, body snippet, or post body
    alt_text_description TEXT,                 -- Plain text description metadata (no binaries)
    author_handle TEXT,                        -- Author, repo owner, or channel handle
    run_id TEXT,                               -- Traceability to execution run
    harvested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    processing_status TEXT DEFAULT 'pending' CHECK (processing_status IN ('pending', 'embedded', 'rejected', 'archived')),
    FOREIGN KEY (run_id) REFERENCES harvest_runs(run_id)
);

-- Performance Indexes for Bear Mode Vector Handshake
CREATE INDEX IF NOT EXISTS idx_harvest_status ON harvest_candidates (processing_status);
CREATE INDEX IF NOT EXISTS idx_harvest_domain ON harvest_candidates (domain_category);
