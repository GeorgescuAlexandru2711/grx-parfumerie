# GrX Parfums — Issue Tracking & User Stories

This document outlines the agile backlog, sprint planning, and completed user stories for **GrX Parfums (An online perfumery for curated fragrances)**.

---

## Team Ownership Matrix (Presentation 1 · Slide 6)

| Ticket ID | Requirement Code | Story / Feature Title | Assigned Owner | Status |
|:---|:---|:---|:---|:---|
| **GRX-01** | `P1-INIT` | Project skeleton, Docker Compose, PostgreSQL & environment config | Alexandru | Done |
| **GRX-02** | `A4` | User accounts, Argon2 password hashing & customer profile | Alexandru | Done |
| **GRX-03** | `A1` | Curated fragrance catalogue: categories, brands, notes & size variants | Alexandru | Done |
| **GRX-04** | `A2` | Olfactory search & faceted family filtering | Alexandru | Done |
| **GRX-05** | `A3` | Session-based shopping bag & complimentary 2 discovery samples | Alexandru | Done |
| **GRX-06** | `B5` | Server-side validated promotional discount coupons | Alexandru | Done |
| **GRX-07** | `A5` | Multi-step checkout with delivery address and shipping rules | Alexandru | Done |
| **GRX-08** | `A7` | Concurrency-safe stock management using PostgreSQL row locks (`select_for_update`) | Alexandru | Done |
| **GRX-09** | `A6` | Stripe test mode checkout & asynchronous webhook confirmation | Alexandru | Done |
| **GRX-10** | `A8` | Customer order history & real-time delivery status tracking | Alexandru | Done |
| **GRX-11** | `A9` | Custom-built Administration Command Center (not default Django admin) | Alexandru | Done |
| **GRX-12** | `B3` | Verified buyer review gate & olfactory star ratings | Alexandru | Done |
| **GRX-13** | `A10` | Security hardening: Argon2, strict CSRF tokens & security headers | Alexandru | Done |
| **GRX-14** | `A11` | Responsive luxury perfume UI in Tailwind CSS (tested down to 360px) | Alexandru | Done |
| **GRX-15** | `A12` | Automated pytest suite: concurrency stress test & webhook simulation | Alexandru | Done |

---

## Detailed User Stories

### [GRX-01] Dockerized Infrastructure & Project Foundation
* **Owner:** Georgescu Alexandru
* **Story:** As a developer/examiner, I want to start the full application and PostgreSQL database with one command (`docker compose up --build`) so that evaluation is reproducible and zero-friction.
* **Acceptance Criteria:**
  - `docker-compose.yml` orchestrating `web` and `postgres:16-alpine` with healthcheck.
  - Multi-stage `Dockerfile` with Python 3.11-slim.
  - `.env.example` and automatic database migrations via `entrypoint.sh`.

### [GRX-02] User Authentication & Security Profile (A4, A10)
* **Owner:** Georgescu Alexandru
* **Story:** As an online shopper, I want to register and sign in securely with my email and password so my shipping addresses and fragrance orders are saved.
* **Acceptance Criteria:**
  - Custom `User` model with email login and Argon2 password hashing.
  - Profile editing for Romanian delivery addresses (County/Sector, City, Postal Code).

### [GRX-03] Curated Fragrance Catalog (A1)
* **Owner:** Georgescu Alexandru
* **Story:** As a fragrance lover, I want to browse perfumes organized by category (Women, Men, Unisex, Gift sets) and scent family, inspect the 3-tier olfactory pyramid (Top, Heart, Base notes), and pick bottle sizes (10ml Travel, 50ml, 100ml).
* **Acceptance Criteria:**
  - 30+ curated luxury & niche fragrances in seed script.
  - `ProductVariant` model storing size in ml, price in RON, SKU, and independent inventory stock.

### [GRX-04] Basic & Olfactory Search (A2)
* **Owner:** Georgescu Alexandru
* **Story:** As a shopper, I want to search fragrances by title, brand, note (e.g. Saffron, Amber, Bergamot), and filter by fragrance family so I can find scents matching my taste without smelling them first.
* **Acceptance Criteria:**
  - Multi-field `Q` search query across title, brand, description, and notes.

### [GRX-05] Shopping Bag & Complimentary Samples (A3)
* **Owner:** Georgescu Alexandru
* **Story:** As a customer, I want to add items to my cart, adjust quantities up to available stock, and pick 2 free discovery vials (Douglas.ro inspiration).
* **Acceptance Criteria:**
  - Session cart calculation with free delivery threshold (300 RON).
  - Choice of up to 2 complimentary fragrance samples.

### [GRX-06] Promotional Coupon System (B5)
* **Owner:** Georgescu Alexandru
* **Story:** As a shopper, I want to apply discount codes (e.g., `WELCOME10`, `LUXURY20`) and have them validated strictly on the server.
* **Acceptance Criteria:**
  - Server-side percentage discounts calculated before taxes & shipping.

### [GRX-07] Checkout Flow (A5)
* **Owner:** Georgescu Alexandru
* **Story:** As a customer, I want to review my shipping details and order breakdown before being redirected to payment.
* **Acceptance Criteria:**
  - Form validation for Romanian addresses and contact details.
  - Atomic pending order creation.

### [GRX-08] Concurrency-Safe Stock Management (A7)
* **Owner:** Georgescu Alexandru
* **Story:** As a store owner, I want to guarantee that two simultaneous shoppers cannot buy the last unit of a fragrance at the same time.
* **Acceptance Criteria:**
  - `create_order_from_cart` uses `select_for_update()` inside `transaction.atomic()`.
  - Automated concurrency unit test simulating parallel checkouts.

### [GRX-09] Stripe Test Mode & Webhook Integration (A6)
* **Owner:** Georgescu Alexandru
* **Story:** As a customer, I want to pay securely via Stripe, and as a store owner, orders must become `PAID` only when the asynchronous webhook confirms the payment.
* **Acceptance Criteria:**
  - Stripe Checkout Session creation with line items in RON.
  - Webhook endpoint handling `checkout.session.completed` with signature validation.
  - Interactive Sandbox testing mode with local simulator.

### [GRX-10] Order History Portal (A8)
* **Owner:** Georgescu Alexandru
* **Story:** As a customer, I want an order history page to track status (Pending, Paid, Shipped, Delivered) and view past purchase receipts.
* **Acceptance Criteria:**
  - Authenticated customer portal listing past orders with item snapshots and status badges.

### [GRX-11] Custom-Built Administration Command Center (A9)
* **Owner:** Georgescu Alexandru
* **Story:** As store administrators, Alexandru and Iannis want a custom-built dashboard (not default Django admin) to monitor revenue KPIs, manage perfumes and bottle sizes, restock low inventory, and update order statuses.
* **Acceptance Criteria:**
  - KPI overview: gross revenue, order volume, low-stock alerts, customer count.
  - Full CRUD for products, size variants, and prices.
  - Order status workflow management and quick inventory replenishment.

### [GRX-12] Verified Buyer Fragrance Reviews (B3)
* **Owner:** Georgescu Alexandru
* **Story:** As a shopper, I want authentic reviews written only by customers who actually bought the fragrance.
* **Acceptance Criteria:**
  - Review submission gated to users who have a confirmed `paid` order for that specific product.

### [GRX-13] Security Hardening (A10)
* **Owner:** Georgescu Alexandru
* **Story:** As the security engineer, I want the system hardened against common web vulnerabilities.
* **Acceptance Criteria:**
  - Argon2 password hashing as primary hasher.
  - Strict CSRF protection on forms and state-changing endpoints.
  - XSS, clickjacking, and session protection headers configured.

### [GRX-14] Responsive Luxury UI (A11)
* **Owner:** Georgescu Alexandru
* **Story:** As a mobile customer, I want the perfumery website to look elegant, luxurious, and render flawlessly on 360px mobile screens as well as 4K monitors.
* **Acceptance Criteria:**
  - Dark obsidian, warm gold, and creamy ivory palette.
  - Mobile responsive drawer, filters, and cards.

### [GRX-15] Automated Test Suite (A12)
* **Owner:** Georgescu Alexandru
* **Story:** As a quality engineer, I want automated tests running via `pytest` to guarantee reliability across catalog, auth, cart, payments, and concurrent stock transactions.
* **Acceptance Criteria:**
  - Pytest tests covering auth, catalog, cart, webhook, and multi-threaded concurrency locking.

