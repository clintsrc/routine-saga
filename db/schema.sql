-- Run:
--   psql -U postgres -f db/schema.sql
--   python manage.py migrate

-- DROP DATABASE
DROP DATABASE IF EXISTS routinesaga_db;

-- CREATE DATABASE
CREATE DATABASE routinesaga_db;