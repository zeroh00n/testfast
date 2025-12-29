-- MySQL 스키마 및 샘플 데이터
CREATE DATABASE IF NOT EXISTS shopdb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE shopdb;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  category VARCHAR(100) NOT NULL,
  price DECIMAL(10,2) NOT NULL
);

CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES orders(id),
  CONSTRAINT fk_items_product FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO users (name) VALUES
  ('홍길동'),
  ('김철수'),
  ('이영희');

INSERT INTO products (name, category, price) VALUES
  ('게이밍 마우스', '디지털/가전', 39000),
  ('무선 키보드', '디지털/가전', 45000),
  ('27인치 모니터', '디지털/가전', 229000),
  ('운동화 러닝화', '패션/의류', 89000),
  ('면 티셔츠', '패션/의류', 19000),
  ('원두 커피 1kg', '식품', 29000),
  ('프리미엄 녹차', '식품', 25000);

INSERT INTO orders (user_id) VALUES
  (1), (1), (2), (2), (3);

INSERT INTO order_items (order_id, product_id, quantity) VALUES
  (1, 1, 1),
  (1, 2, 1),
  (1, 3, 1),
  (2, 6, 2),
  (3, 1, 1),
  (3, 4, 1),
  (4, 4, 1),
  (4, 5, 2),
  (5, 6, 1),
  (5, 7, 1);
