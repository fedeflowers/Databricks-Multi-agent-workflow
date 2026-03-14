-- Catalogs and Schemas
CREATE CATALOG IF NOT EXISTS prada_catalog;
USE CATALOG prada_catalog;
CREATE SCHEMA IF NOT EXISTS plsa;
CREATE SCHEMA IF NOT EXISTS monitoring;
USE SCHEMA plsa;

-- Store Management Mock Tables
CREATE TABLE IF NOT EXISTS products (
    product_id STRING,
    product_name STRING,
    category STRING,
    price DOUBLE,
    in_stock INT
);
INSERT INTO products VALUES
    ('p001', 'Laptop', 'Electronics', 900.0, 20),
    ('p002', 'Shampoo', 'Health & Beauty', 8.5, 50);

CREATE TABLE IF NOT EXISTS sales (
    sale_id STRING,
    product_id STRING,
    user_id STRING,
    quantity INT,
    sale_amount DOUBLE,
    sale_date DATE
);
INSERT INTO sales VALUES
    ('s001', 'p001', 'u001', 1, 900.0, '2024-06-03'),
    ('s002', 'p002', 'u002', 5, 42.5, '2024-06-04');

CREATE TABLE IF NOT EXISTS inventory (
    product_id STRING,
    warehouse STRING,
    stock_level INT
);
INSERT INTO inventory VALUES
    ('p001', 'WH1', 10),
    ('p002', 'WH2', 30);

CREATE TABLE IF NOT EXISTS employees (
    employee_id STRING,
    name STRING,
    role STRING,
    hire_date DATE
);
INSERT INTO employees VALUES
    ('e001', 'Carol', 'Manager', '2020-01-15'),
    ('e002', 'David', 'Cashier', '2022-03-20');

-- Vector Search Index Tables
CREATE TABLE IF NOT EXISTS guidelines_index (
    guideline_id STRING,
    guideline_text STRING,
    embedding ARRAY<DOUBLE>
);
INSERT INTO guidelines_index VALUES
    ('g001', 'Always validate inputs.', array(0.12, 0.34, 0.56)),
    ('g002', 'Ensure data privacy.', array(0.21, 0.43, 0.65));
