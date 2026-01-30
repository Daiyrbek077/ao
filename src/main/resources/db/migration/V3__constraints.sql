ALTER TABLE sales
    ADD CONSTRAINT fk_sales_customer FOREIGN KEY (customer_id) REFERENCES customers(id);

ALTER TABLE sale_items
    ADD CONSTRAINT fk_sale_items_sale FOREIGN KEY (sale_id) REFERENCES sales(id),
    ADD CONSTRAINT fk_sale_items_book FOREIGN KEY (book_id) REFERENCES books(id);

ALTER TABLE my_books
    ADD CONSTRAINT fk_my_books_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    ADD CONSTRAINT fk_my_books_book FOREIGN KEY (book_id) REFERENCES books(id);

ALTER TABLE loyalty_points
    ADD CONSTRAINT fk_loyalty_points_customer FOREIGN KEY (customer_id) REFERENCES customers(id);
