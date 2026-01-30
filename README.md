# SmartBook Backend

SmartBook is a multi-tenant SaaS ERP backend for bookstores. Each shop is isolated by `shop_id` while sharing the same PostgreSQL database.

## Features

- JWT authentication/authorization with roles (ADMIN, CASHIER, CUSTOMER)
- Multi-tenant filtering using `shop_id`
- POS workflows (sales, bonuses, receipts)
- Inventory and book management
- Loyalty program and MyBooks
- Google Books ISBN lookup
- Analytics endpoints
- Flyway migrations
- OpenAPI/Swagger at `/swagger-ui.html`

## Requirements

- Java 17
- Maven 3.9+
- PostgreSQL 16+

## Configuration

Update `src/main/resources/application.yml` for your PostgreSQL connection and JWT secret.

## Running locally

```bash
./mvnw spring-boot:run
```

## Tests

```bash
./mvnw test
```

## API

- Auth: `/api/auth/**`
- Admin: `/api/admin/**`
- POS: `/api/pos/**`
- Customer: `/api/customer/**`

Swagger UI: `http://localhost:8080/swagger-ui.html`
