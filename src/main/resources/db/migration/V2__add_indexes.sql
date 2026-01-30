CREATE INDEX idx_users_shop ON users(shop_id);
CREATE INDEX idx_books_shop ON books(shop_id);
CREATE INDEX idx_customers_shop ON customers(shop_id);
CREATE INDEX idx_sales_shop ON sales(shop_id);
CREATE INDEX idx_sale_items_sale ON sale_items(sale_id);
CREATE INDEX idx_my_books_customer ON my_books(customer_id);
CREATE INDEX idx_loyalty_points_customer ON loyalty_points(customer_id);
