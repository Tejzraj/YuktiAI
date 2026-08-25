-- Migration: Add columns needed for Travel Planner & Hotels module (Simran)
-- Run this AFTER init.sql has already created the base tables.
-- Usage: docker exec -i yuktiai_postgres psql -U postgres -d yuktiai < alter_hotels_travel.sql

ALTER TABLE hotels ADD COLUMN IF NOT EXISTS rating NUMERIC(2,1);
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS facilities TEXT[];

ALTER TABLE travel_options ADD COLUMN IF NOT EXISTS from_city VARCHAR(100);
