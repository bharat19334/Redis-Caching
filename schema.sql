-- 1. Products table create karein
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC NOT NULL,
    category TEXT NOT NULL,
    stock INT NOT NULL
);

-- 2. 100 Sample Products generate karke insert karein
INSERT INTO products (name, price, category, stock)
SELECT 
    'Product Item ' || i,
    ROUND((RANDOM() * 5000 + 99)::numeric, 2),
    CASE (i % 5)
        WHEN 0 THEN 'Electronics'
        WHEN 1 THEN 'Accessories'
        WHEN 2 THEN 'Audio'
        WHEN 3 THEN 'Storage'
        ELSE 'Furniture'
    END,
    FLOOR(RANDOM() * 90 + 10)::int
FROM generate_series(1, 100) AS s(i);