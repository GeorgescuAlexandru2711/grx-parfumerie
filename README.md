# GrX Parfums — Online Perfumery for Curated Fragrances

> **E-Commerce Semester Project · Presentation 1 to Presentation 3**  
> **Team:** Georgescu Alexandru & Georgescu Alexandru  
> **Institution:** University of Craiova (UCV)

[![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Stripe](https://img.shields.io/badge/Stripe-6772E5?style=for-the-badge&logo=stripe&logoColor=white)](https://stripe.com/)
[![Docker](https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)

---

## 1. Project Vision & The Niche

**GrX Parfums** is a luxury online perfumery targeting Romanian fragrance enthusiasts aged 22–40 who purchase perfume online—often as gifts—and require guided discovery without smelling the perfume in person.

### What We Adopted From Real Market Leaders
* **From Notino.ro:** Detailed fragrance pyramid breakdown (Top, Heart, Base notes) and guided discovery without catalog overwhelm.
* **From Douglas.ro:** Two complimentary discovery vials with every order, transparent delivery policies, and curated luxury packaging.
* **From Sephora.ro:** Customer ratings and reviews gated strictly to **verified buyers (B3)**, plus server-side validated promotional coupon codes (**B5**).

---

## 2. Team Split & Responsibility Matrix (A1–A12)

| Requirement Code | Feature Area | Primary Contributor | Key Implementation Highlights |
|:---|:---|:---|:---|
| **A1** | Curated Fragrance Catalog | **Georgescu Alexandru** | 30+ products across 4 categories (Women, Men, Unisex, Gift sets) with 3-tier olfactory pyramid & travel sizes. |
| **A2** | Olfactory Search | **Georgescu Alexandru** | Search across titles, brands, scent notes, and family filters. |
| **A3** | Shopping Bag | **Georgescu Alexandru** | Session-based cart with 2 free discovery samples & free shipping threshold. |
| **A4** | User Accounts | **Georgescu Alexandru** | Custom user model with Argon2 password hashing and Romanian address profiles. |
| **A5** | Checkout Flow | **Georgescu Alexandru** | Multi-step address collection, summary validation, and atomic order creation. |
| **A6** | Sandbox Payment & Webhooks | **Georgescu Alexandru** | Stripe Checkout Session & Webhook receiver updating orders to `PAID`. |
| **A7** | Stock Management & Concurrency | **Georgescu Alexandru** | PostgreSQL row-level locking (`select_for_update`) to prevent double-selling the last unit. |
| **A8** | Order History | **Georgescu Alexandru** | Customer dashboard showing order status tracking and past receipts. |
| **A9** | Custom Administration Panel | **Georgescu Alexandru** | **Bespoke admin command center** (not standard Django admin) with KPIs, stock restock, and order workflows. |
| **A10** | Security Hardening | **Georgescu Alexandru** | Argon2 hashing, strict CSRF validation, XSS & Clickjacking prevention headers. |
| **A11** | Responsive Design | **Georgescu Alexandru** | Django templates + Tailwind CSS styled for mobile (360px) to desktop. |
| **A12** | Automated Testing Suite | **Georgescu Alexandru** | `pytest` test suite with automated concurrency simulation and webhook verification. |
| **B3** | Verified Buyer Reviews | **Georgescu Alexandru** | Review submission strictly gated to verified purchasers. |
| **B5** | Promotional Discount Codes | **Georgescu Alexandru** | Server-side percentage discounts (`WELCOME10`, `LUXURY20`). |

---

## 3. Technology Stack

* **Backend:** Python 3.11, Django 5.1 (ORM, Argon2 password hasher, CSRF security).
* **Frontend:** Django Templates + Tailwind CSS (warm obsidian `#0D0D11`, soft gold `#C5A880`, ivory `#FAF7F2`).
* **Database:** PostgreSQL 16 (Row-level locking `select_for_update` for race-condition prevention).
* **Payments:** Stripe API (Test Mode) + Webhook listener.
* **Testing:** `pytest`, `pytest-django`, multi-threaded concurrency tests.
* **Containerization:** Docker & Docker Compose (`web` + `db` + seed automation).

---

## 4. AI Tools Used

In accordance with semester project guidelines, AI assistance was leveraged transparently for:
* **Architecture & Scaffolding:** Antigravity AI pair programming assistant for designing clean Django modular applications (`accounts`, `catalog`, `cart`, `orders`, `payments`, `reviews`, `dashboard`).
* **Curated Olfactory Data:** Assisting in structuring authentic top, heart, and base notes for 30+ luxury fragrance entries (MFK, Creed, Le Labo, Kilian, Tom Ford, etc.).
* **Concurrency Test Harness:** Designing multi-threaded Python stress tests to verify PostgreSQL row-level locks against race conditions.

---

## 5. Quick Start (One Command Run)

### Option A: Using Docker Compose (Recommended for Teaching Staff)

```bash
# 1. Clone repository
git clone https://github.com/GeorgescuAlexandru2711/grx-parfums.git
cd grx-parfums

# 2. Copy environment file
cp .env.example .env

# 3. Start PostgreSQL and Django Web application
docker compose up --build
```
The application will be accessible at: **http://localhost:8000**  
Migrations and initial catalog seeding run automatically via `entrypoint.sh`.

---

### Option B: Local Development Setup

```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run database migrations
python manage.py migrate

# 4. Seed 30+ curated fragrances and demo users
python manage.py seed_catalog

# 5. Start development server
python manage.py runserver
```

---

## 6. Default Demo Credentials

* **Store Administrator (Custom Admin Panel A9):**
  * **URL:** http://localhost:8000/admin-dashboard/
  * **Email:** `admin@grxparfums.ro`
  * **Password:** `GrXadmin2026!`
* **Verified Customer Account:**
  * **Email:** `alex@example.com`
  * **Password:** `CustomerPass2026!`

---

## 7. Running Automated Tests (A12)

```bash
# Run full test suite with pytest
pytest
```
Tests include:
* Authentication & Argon2 verification
* Catalog filtering & search accuracy
* Shopping bag operations and coupon calculations
* **Concurrency race-condition test:** Simulates simultaneous customer orders on the last stock unit to prove row-level locking works.
* Stripe Webhook payment status transitions

---

## 8. Issue Tracking & Sprint Roadmap

See [TICKETS.md](TICKETS.md) for full sprint stories, acceptance criteria, and git commit mapping.

