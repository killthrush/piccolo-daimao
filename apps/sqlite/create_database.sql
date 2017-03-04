-- Create empty table for piccolo-daimao apps
-- Requires relatively new installation of sqlite3 (tested successfully with 3.11.0)
CREATE TABLE IF NOT EXISTS numbers (key TEXT, value INTEGER DEFAULT 0);
CREATE UNIQUE INDEX IF NOT EXISTS numbers_key_index ON numbers (key);