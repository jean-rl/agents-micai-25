# MCP API Documentation

This section documents the **Trading API** used in the MCP (Model Context Protocol) part of the tutorial.

---

## Quick workflow (human summary)

1. **Register** a user → you receive a `token`.
2. Save the `token` locally (this is your identity / API key).
3. **Start the simulation** (teacher) to open the market.
4. Ask **current market** or **history** endpoints to read prices & news.
5. **Buy** / **Sell** using your `token`.
6. Check **account** to see balance & positions.

---

# Endpoints

> All endpoints live under the API base URL (`https://axum-todo-list-giz6.shuttle.app`).
> Methods that take JSON expect `Content-Type: application/json`.

---

## 1) `POST /register`

**What it does:** create a new demo account and receive a `token` to authenticate later requests.

**Inputs (JSON)**

* `username` (string) — **required**
  Example:

```json
{ "username": "alice" }
```

**Success output (201 / JSON)**

* `token`: string you must include in future requests (treat like a password).
* `balance`: starting cash balance (demo).

```json
{
  "token": "alice_6b1f8b8d-....",
  "balance": 1000000.0
}
```

**Common errors**

* `400 Bad Request` — missing `username` or invalid payload.
* `500 Internal Server Error` — DB or server issue.

**Human note:** Save the `token` securely (keychain, file, or the example `TokenStore` in the tutorial).

---

## 2) `POST /account`

**What it does:** returns account info (balance and current positions). Requires `token`.

**Inputs (JSON)**

* `token` (string) — **required**
  Example:

```json
{ "token": "alice_6b1f8b8d-...." }
```

**Success output (200 / JSON)**

```json
{
  "balance": 999500.0,
  "positions": [
    {
      "id": 7,
      "user_id": 3,
      "stock_symbol": "AAPL",
      "quantity": 5,
      "avg_price": 100.00
    }
  ]
}
```

**Common errors**

* `400 Bad Request` — missing token field.
* `401 Unauthorized` — invalid token.
* `500 Internal Server Error`.

**Human note:** `positions` is a list of holdings. `avg_price` is the average buy price for that holding.

---

## 3) `GET /market`

**What it does:** returns the current market round, the prices for each stock, and the current news blurb.

**Inputs (query params)**

* none (the server uses its internal `current_round`).

**Success output (200 / JSON)**

```json
{
  "round": 3,
  "stocks": [
    {"symbol":"AAPL","price":107.5},
    {"symbol":"TSLA","price":53.6},
    {"symbol":"JPM","price":187.0},
    {"symbol":"PFE","price":77.3},
    {"symbol":"XOM","price":154.5}
  ],
  "news": "Market news for round 3: Tech sector shows mixed trend..."
}
```

**Common errors**

* `400 Bad Request` — if the simulation is closed (not running).

**Human note:** Use this endpoint to show the agent or student the prices used to compute buy/sell trades.

---

## 4) `GET /market/history`

**What it does:** returns historical prices and news up to the current round.

**Inputs (query params)**

* none

**Success output (200 / JSON)**

```json
{
  "prices": [
    {"round":1,"stocks":[{"symbol":"AAPL","price":102.5}, ...]},
    {"round":2,"stocks":[...]}
  ],
  "news_history": [
    [1, "Market news for round 1: ..."],
    [2, "Market news for round 2: ..."]
  ]
}
```

**Human note:** Useful for plotting price evolution or for agents that use past rounds to make decisions.

---

## 5) `POST /buy`

**What it does:** buy `quantity` shares of `stock_symbol` for the authenticated user (current round price).

**Inputs (JSON)**

* `token` (string) — **required**
* `stock_symbol` (string) — **required**, one of `AAPL`, `TSLA`, `JPM`, `PFE`, `XOM`
* `quantity` (integer) — **required**, number of shares to buy
  Example:

```json
{ "token":"alice_...", "stock_symbol":"AAPL", "quantity": 10 }
```

**Success output (200 / JSON)**

```json
{
  "success": true,
  "message": "Bought 10 shares of AAPL at $107.50",
  "balance": 998925.0
}
```

**Common errors**

* `400 Bad Request` — invalid symbol, insufficient funds, or simulation closed.
* `401 Unauthorized` — token invalid.

**Human note:** Cost = `price * quantity`. If you don't have cash → request is rejected.

---

## 6) `POST /sell`

**What it does:** sell `quantity` shares of `stock_symbol` from the user's positions at current market price.

**Inputs (JSON)**

* `token` (string) — **required**
* `stock_symbol` (string) — **required**
* `quantity` (integer) — **required**
  Example:

```json
{ "token":"alice_...", "stock_symbol":"AAPL", "quantity": 5 }
```

**Success output (200 / JSON)**

```json
{
  "success": true,
  "message": "Sold 5 shares of AAPL at $107.50",
  "balance": 999500.0
}
```

**Common errors**

* `400 Bad Request` — insufficient shares, invalid symbol, or simulation closed.
* `401 Unauthorized`.

**Human note:** If you sell all shares of a position, the position is removed.

---

# Error codes (simple guide)

* `200` — OK / success
* `201` — Created (register)
* `400` — Bad request (missing/invalid inputs, simulation closed, insufficient funds)
* `401` — Unauthorized (invalid token)
* `500` — Server error

---

# Examples (quick, copyable)

### curl — register

```bash
curl -X POST https://axum-todo-list-giz6.shuttle.app/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice"}'
```

### httpx (python) — get account

```python
import httpx
resp = httpx.post("https://axum-todo-list-giz6.shuttle.app/account", json={"token": TOKEN})
print(resp.json())
```