-- Sample database schema for AskPostgres demo
-- This creates some sample tables with data for testing

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50),
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL
);

-- Insert sample data
INSERT INTO users (name, email, created_at) VALUES
('John Doe', 'john@example.com', NOW() - INTERVAL '30 days'),
('Jane Smith', 'jane@example.com', NOW() - INTERVAL '25 days'),
('Bob Johnson', 'bob@example.com', NOW() - INTERVAL '20 days'),
('Alice Brown', 'alice@example.com', NOW() - INTERVAL '15 days'),
('Charlie Wilson', 'charlie@example.com', NOW() - INTERVAL '10 days');

INSERT INTO products (name, description, price, category, stock_quantity) VALUES
('Laptop Pro', 'High-performance laptop for professionals', 1299.99, 'Electronics', 50),
('Wireless Mouse', 'Ergonomic wireless mouse', 29.99, 'Electronics', 200),
('Coffee Mug', 'Ceramic coffee mug with logo', 12.99, 'Accessories', 100),
('Notebook', 'Premium leather-bound notebook', 24.99, 'Stationery', 75),
('Desk Lamp', 'LED desk lamp with adjustable brightness', 89.99, 'Furniture', 30);

INSERT INTO orders (user_id, total_amount, status, created_at) VALUES
(1, 1329.98, 'completed', NOW() - INTERVAL '28 days'),
(2, 42.98, 'completed', NOW() - INTERVAL '23 days'),
(3, 89.99, 'pending', NOW() - INTERVAL '18 days'),
(4, 37.98, 'completed', NOW() - INTERVAL '13 days'),
(5, 1299.99, 'shipped', NOW() - INTERVAL '8 days');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1299.99),
(1, 2, 1, 29.99),
(2, 2, 1, 29.99),
(2, 3, 1, 12.99),
(3, 5, 1, 89.99),
(4, 3, 1, 12.99),
(4, 4, 1, 24.99),
(5, 1, 1, 1299.99);
