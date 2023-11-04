CREATE EXTENSION Postgis;

CREATE TABLE driver (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
	status int NOT NULL,
    is_verified BOOLEAN NOT NULL,
    date_of_birth DATE NOT NULL,
	location geography(point,4326),
	pass_hash VARCHAR NOT NULL,
	vehicle_type int not null,
	rating DECIMAL(3, 1) not null default 0.0
);


CREATE TABLE rider (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    date_of_birth DATE NOT NULL,
	pass_hash VARCHAR NOT NULL,
	rating DECIMAL(3, 1) not null default 0.0
);

CREATE TABLE payment (
    id SERIAL PRIMARY KEY,
    amount DECIMAL NOT NULL,
	payment_date TIMESTAMP NOT NULL
);

ALTER TABLE payment
	ADD column rider_id INT REFERENCES rider(id);

CREATE TABLE earning (
    id SERIAL PRIMARY KEY,
    amount DECIMAL NOT NULL,
	earning_date TIMESTAMP NOT NULL SET DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE earning
	ADD column driver_id INT REFERENCES driver(id);

CREATE TABLE failed_payment (
    id SERIAL PRIMARY KEY,
    amount DECIMAL NOT NULL,
	payment_date TIMESTAMP NOT NULL
);

ALTER TABLE failed_payment
	ADD column rider_id INT REFERENCES rider(id);

CREATE TABLE trip (
	origin geography(point,4326) NOT NULL,
	destination geography(point,4326) NOT NULL,
	trip_time TIMESTAMP,
	booking_id VARCHAR NOT NULL,
);

ALTER TABLE trip
	ADD column rider_id INT REFERENCES rider(id);
ALTER TABLE trip
	ADD column payment_id INT REFERENCES payment(id) UNIQUE;

-- insert into rider (first_name,last_name,email, date_of_birth, pass_hash) values ('John', 'Doe', 'jd@gmail.com', DATE '1980-01-22', '$2b$12$XQIm.xErFOf89Hk2aACf9uYGCl2xKtOC0YWL3P5PBwABr5FsaQdWC');
-- insert into rider (first_name,last_name,email, date_of_birth, pass_hash) values ('Lily', 'Smith', 'ls@gmail.com', DATE '1990-01-22', '$2b$12$XQIm.xErFOf89Hk2aACf9uYGCl2xKtOC0YWL3P5PBwABr5FsaQdWC');
-- insert into driver (first_name, last_name, email, status, is_verified, date_of_birth, location, pass_hash, vehicle_type) values ('Sam', 'Hum', 'sh@gmail.com', 'active', true, DATE '1980-01-22', ST_SetSRID(ST_MakePoint(1, 1), 4326), '$2b$12$XQIm.xErFOf89Hk2aACf9uYGCl2xKtOC0YWL3P5PBwABr5FsaQdWC', 0)
-- insert into driver (first_name, last_name, email, status, is_verified, date_of_birth, location, pass_hash, vehicle_type) values ('Tim', 'Hort', 'th@gmail.com', 'active', true, DATE '1982-01-12', ST_SetSRID(ST_MakePoint(1, 100), 4326), '$2b$12$XQIm.xErFOf89Hk2aACf9uYGCl2xKtOC0YWL3P5PBwABr5FsaQdWC', 0)
