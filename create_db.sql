DROP DATABASE IF EXISTS slabcode_db;
CREATE DATABASE slabcode_db;
CREATE USER slabcode_user WITH PASSWORD 'slabcode_pass';
ALTER ROLE slabcode_user SET client_encoding TO 'utf8';
ALTER ROLE slabcode_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE slabcode_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE slabcode_db TO slabcode_user;
