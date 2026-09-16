CREATE TABLE IF NOT EXISTS scam_campaign_jobs (
	id TEXT PRIMARY KEY,
	title TEXT NOT NULL,
	company TEXT NOT NULL,
	location TEXT NOT NULL,
	salary TEXT,
	snippet TEXT NOT NULL,
	contact_phone TEXT,
	contact_email TEXT,
	payment_id TEXT,
	source TEXT,
	created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
