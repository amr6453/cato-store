# Cato-Store API reference (frontend)

This document shows quick example queries and mutations for both the REST API (for convenience) and the GraphQL API (recommended for frontend integration).

## GraphQL (recommended)

Endpoint: `/graphql/` (GraphiQL enabled in dev)

Authentication: use session auth or send token via headers depending on your setup (e.g. `Authorization: Token <token>` for DRF token auth). GraphQL uses `info.context` to access the Django request.

Example: list products (first 10)

query:
```
query ListProducts($first: Int) {
  products(first: $first) {
    id
    name
    slug
    price
    stockQuantity
    isActive
    images {
      id
      order
      altText
      image
    }
  }
}
```
variables:
```
{ "first": 10 }
```

Example: product detail by slug

```
query ProductDetail($slug: String!) {
  product(slug: $slug) {
    id
    name
    description
    price
    stockQuantity
    images { id image altText }
  }
}
```

Guest create order (no auth)

```
mutation GuestCreateOrder($items: [OrderItemInput!]!) {
  guestCreateOrder(items: $items) {
    ok
    message
    order { id totalAmount status }
  }
}
```

Authenticated create order (must be logged in or send token header)

```
mutation CreateOrder($items: [OrderItemInput!]!) {
  createOrder(items: $items) {
    ok
    message
    order { id totalAmount status }
  }
}
```

Order detail (authenticated)

```
query OrderDetail($id: Int!) {
  order(id: $id) {
    id
    status
    totalAmount
    items { id product { id name price } quantity price }
  }
}
```

Notes:
- `OrderItemInput` shape: `{ productId: Int!, quantity: Int! }` (GraphQL names are `productId` and `quantity`).
- For authenticated GraphQL requests, include any authentication token header your server expects (e.g. `Authorization: Token <token>`).

## REST (existing endpoints)

Base: `/api/`

Products
- `GET /api/products/` — list products (DRF pagination). Query params: `search`, `ordering`.
- `GET /api/products/<id>/` — product detail.

Auth
- `POST /api/auth/register/` — register. Returns token.
- `POST /api/auth/login/` — login. Returns token.
- `GET/PATCH /api/auth/profile/me/` — get/update current profile (requires token).

Orders
- `POST /api/orders/create_from_payload/` — create order from JSON payload (authenticated or guest depending on implementation).
- `POST /api/orders/create_from_cart/` — create order from session cart (server-side session required).

Authentication (JWT)
- Obtain token (pair): `POST /api/token/` with `{ "username": "...", "password": "..." }` returns `access` and `refresh` tokens.
- Refresh token: `POST /api/token/refresh/` with `{ "refresh": "<refresh_token>" }` returns a new `access`.

To use JWT with GraphQL, include the header `Authorization: Bearer <access_token>` when calling `/graphql/`.

Password reset (API)
- Request reset: `POST /api/auth/password_reset/` with `{ "email": "user@example.com" }`. This sends a reset email (local dev email backend stores the message in memory).
- Confirm reset: `POST /api/auth/password_reset/confirm/` with `{ "uid": "<user_id>", "token": "<token>", "new_password": "..." }`.

The dev email backend keeps emails in memory; for testing, you can inspect Django's `django.core.mail.outbox` in tests.

Payments
- `POST /api/payments/stripe/webhook/` — webhook endpoint for payment events (simulated HMAC verification in dev).

## Helpful Frontend examples

Fetch GraphQL product list using `fetch` (JS):

```js
async function fetchProducts() {
  const query = `query { products(first: 10) { id name price slug } }`;
  const res = await fetch('/graphql/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
  return res.json();
}
```

Create authenticated order example (send token header):

```js
const mutation = `mutation($items: [OrderItemInput!]!) { createOrder(items: $items) { ok message order { id totalAmount } } }`;
const res = await fetch('/graphql/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Token YOUR_TOKEN'
  },
  body: JSON.stringify({ query: mutation, variables: { items: [{ productId: 1, quantity: 2 }] } })
});
``` 

## Notes & recommendations
- Use GraphQL for flexible data shapes and to reduce round-trips (product lists with images, cart + user data in one request).
- For file uploads (avatars/product images) we currently use REST endpoints (DRF). If you need GraphQL file uploads, we can add the multipart spec and server-side support.

---

If you'd like, I can also:
- Add a short `api_samples.http` file (for VS Code REST Client) with runnable requests.
- Add example GraphQL queries to the repo `docs/` folder or wire `/api/docs/` to show examples.

