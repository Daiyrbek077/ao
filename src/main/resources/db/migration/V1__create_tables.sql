CREATE TABLE shops (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    shop_id BIGINT NOT NULL
);

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(32) NOT NULL,
    active BOOLEAN NOT NULL,
    shop_id BIGINT NOT NULL
);

CREATE TABLE books (
    id BIGSERIAL PRIMARY KEY,
    isbn VARCHAR(32) NOT NULL,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    image_url VARCHAR(512),
    price NUMERIC(12,2) NOT NULL,
    stock INT NOT NULL,
    shop_id BIGINT NOT NULL
);

CREATE TABLE customers (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    telegram_id VARCHAR(255),
    phone VARCHAR(64),
    bonus_balance INT NOT NULL,
    shop_id BIGINT NOT NULL
);

CREATE TABLE sales (
    id BIGSERIAL PRIMARY KEY,
    payment_type VARCHAR(32) NOT NULL,
    customer_id BIGINT,
    total_amount NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    shop_id BIGINT NOT NULL
);

CREATE TABLE sale_items (
    id BIGSERIAL PRIMARY KEY,
    sale_id BIGINT NOT NULL,
    book_id BIGINT NOT NULL,
    quantity INT NOT NULL,
    price NUMERIC(12,2) NOT NULL,
    shop_id BIGINT NOT NULL
);

CREATE TABLE my_books (
    id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    book_id BIGINT NOT NULL,
    status VARCHAR(64) NOT NULL,
    purchased_at TIMESTAMPTZ NOT NULL,
    shop_id BIGINT NOT NULL
);

CREATE TABLE loyalty_points (
    id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    points INT NOT NULL,
    reason VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    shop_id BIGINT NOT NULL
);
