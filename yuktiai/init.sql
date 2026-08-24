-- 1. Categories Table
CREATE TABLE festival_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- 2. Master Festivals Table
CREATE TABLE festivals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    local_name VARCHAR(150),
    district VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    latitude NUMERIC(10, 8),
    longitude NUMERIC(11, 8),
    start_date DATE,
    end_date DATE,
    timings VARCHAR(100),
    category_id INT REFERENCES festival_categories(id),
    short_description TEXT,
    cultural_significance TEXT,
    history_origin TEXT,
    major_attractions TEXT[],
    local_food TEXT[],
    activities TEXT[],
    expected_footfall INT,
    official_website VARCHAR(255)
);

-- 3. Media & Supporting Tables
CREATE TABLE festival_images (
    id SERIAL PRIMARY KEY,
    festival_id INT REFERENCES festivals(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL
);

CREATE TABLE travel_options (
    id SERIAL PRIMARY KEY,
    festival_id INT REFERENCES festivals(id) ON DELETE CASCADE,
    mode VARCHAR(50), -- Bus, Train, Car
    estimated_cost NUMERIC(10,2),
    duration VARCHAR(50)
);

CREATE TABLE hotels (
    id SERIAL PRIMARY KEY,
    festival_id INT REFERENCES festivals(id) ON DELETE CASCADE,
    hotel_name VARCHAR(150),
    distance_km NUMERIC(5,2),
    price_per_night NUMERIC(10,2),
    booking_url TEXT
);