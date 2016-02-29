CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ts TIMESTAMP DEFAULT current_timestamp,
  body TEXT
);
