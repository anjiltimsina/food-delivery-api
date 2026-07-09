# Food Delivery API

A backend REST API for a food delivery platform, built with FastAPI, PostgreSQL, and async SQLAlchemy.

Live API docs: https://food-delivery-api-y0jq.onrender.com/docs

Note: this is hosted on Render's free tier, which spins down after inactivity. The first request after a period of inactivity can take 30-50 seconds to respond while the server wakes up. This is a hosting limitation, not a bug in the app.

## Tech Stack

- FastAPI (async)
- PostgreSQL (hosted on Neon)
- SQLAlchemy 2.0 (async)
- Alembic for migrations
- JWT authentication + Google OAuth
- Passlib/Bcrypt for password hashing
- Cloudinary for image uploads
- Brevo for transactional email (HTTP API)
- SlowAPI for rate limiting
- Docker
- Deployed on Render

## Features

- JWT auth with access and refresh tokens
- Google OAuth login
- Email verification on registration
- Role-based access control (Admin, Customer, Restaurant Owner)
- Restaurant management with an admin approval workflow
- Food item management with image uploads
- Cart system
- Order management with status tracking
- Reviews with automatic restaurant rating updates
- Pagination on list endpoints
- Rate limiting on auth endpoints
- Request logging middleware
- Dockerized setup

## Some notes on how this is built

A few things worth mentioning about the design, mostly things I ran into while actually deploying this rather than just running it locally.

Email is sent through Brevo's HTTP API rather than SMTP. Most free hosting tiers, including Render, block outbound SMTP ports to cut down on spam abuse from free accounts, so a normal SMTP connection to Gmail just hangs and times out in production even though it works fine locally. Sending over HTTPS instead avoids that problem.

The database connection pool is configured with pool_pre_ping=True and pool_recycle=300. Neon's pooled connections get closed on their end during idle periods, and without these settings you'll eventually see "connection is closed" errors on requests that come in after some idle time.

Restaurant approval status is checked in more than one place. It's not enough to just filter unapproved restaurants out of the public listing endpoint — the same check needs to happen when someone fetches a food item directly or places an order, otherwise an unapproved restaurant's ID can just be used directly to get around the approval step entirely.

The registration endpoint restricts which roles a user can pick for themselves. Only "customer" and "restaurant_owner" are allowed at signup. Admin accounts are not something you can create through public registration.

Config (base URL, database connection, third-party API keys) is all handled through environment variables, so the same code runs against localhost in development and the live Render URL in production without any code changes.

## Project Structure

```
FoodDeliveryAPI/
├── app/
│   ├── core/
│   │   ├── config.py          # settings loaded from environment variables
│   │   ├── security.py        # JWT, password hashing
│   │   └── dependencies.py    # auth guards, role checks
│   ├── db/
│   │   ├── database.py        # async engine + session
│   │   └── base.py
│   ├── models/                # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── routers/                # route definitions
│   ├── services/                # business logic
│   ├── middleware/
│   │   ├── auth_middleware.py
│   │   ├── logging_middleware.py
│   │   └── rate_limit_middleware.py
│   ├── utils/
│   │   ├── upload.py           # Cloudinary uploads
│   │   └── email.py            # Brevo email
│   └── main.py
├── migrations/
├── .env.example
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Running locally

### With Docker

```bash
git clone https://github.com/anjiltimsina/food-delivery-api.git
cd food-delivery-api
cp .env.example .env
# fill in .env with your own values
docker-compose up --build
docker-compose exec api alembic upgrade head
```

Then open http://localhost:8001/docs

### Without Docker

```bash
git clone https://github.com/anjiltimsina/food-delivery-api.git
cd food-delivery-api
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows

pip install -r requirements.txt
cp .env.example .env
# fill in .env with your own values

alembic upgrade head
uvicorn app.main:app --reload --port 8001
```

Then open http://localhost:8001/docs

## Environment Variables

See .env.example for the full list. At minimum you need:

```
APP_NAME="FoodDeliveryAPI"
DEBUG=False
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

DATABASE_URL=postgresql+asyncpg://user:password@host/dbname

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://your-domain.com/auth/google/callback

BASE_URL=https://your-domain.com

CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

BREVO_API_KEY=your-brevo-api-key
MAIL_FROM=your-verified-sender@example.com
```

## API Overview

### Auth

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | /auth/register | Public | Register (customer or restaurant owner only) |
| POST | /auth/login | Public | Login with email/password |
| POST | /auth/refresh | Public | Refresh access token |
| GET | /auth/verify-email | Public | Verify email via token |
| GET | /auth/me | Authenticated | Get current user |
| GET | /auth/google/login | Public | Google OAuth login |
| GET | /auth/google/callback | Public | Google OAuth callback |

### Restaurants

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | /restaurants/ | Public | List approved restaurants (paginated) |
| GET | /restaurants/{id} | Public | Get a single restaurant |
| GET | /restaurants/admin/all | Admin | List all restaurants, including unapproved |
| POST | /restaurants/ | Restaurant Owner | Create a restaurant |
| PATCH | /restaurants/{id}/approve | Admin | Approve a restaurant |
| PUT | /restaurants/{id} | Owner/Admin | Update restaurant details |
| DELETE | /restaurants/{id} | Owner/Admin | Delete a restaurant |

### Food Items

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | /restaurants/{id}/foods | Public | List food items for a restaurant |
| GET | /restaurants/{id}/foods/{fid} | Public | Get a single food item |
| POST | /restaurants/{id}/foods | Owner/Admin | Add a food item |
| PUT | /restaurants/{id}/foods/{fid} | Owner/Admin | Update a food item |
| DELETE | /restaurants/{id}/foods/{fid} | Owner/Admin | Delete a food item |

### Cart and Orders

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | /cart/ | Customer | View cart |
| POST | /cart/items | Customer | Add item to cart |
| POST | /orders/ | Customer | Place order from cart |
| GET | /orders/my | Customer | View my orders |
| PATCH | /orders/{id}/status | Owner/Admin | Update order status |
| PATCH | /orders/{id}/cancel | Authenticated | Cancel an order |

### Reviews

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | /reviews/restaurant/{id} | Public | Get restaurant reviews |
| POST | /reviews/ | Customer | Leave a review for a delivered order |

Full endpoint list and interactive testing available at /docs.

## Role Permissions

| Feature | Admin | Restaurant Owner | Customer | Public |
|---|---|---|---|---|
| View approved restaurants | Yes | Yes | Yes | Yes |
| Create a restaurant | Yes | Yes | No | No |
| Approve a restaurant | Yes | No | No | No |
| Manage food items | Yes | Own only | No | No |
| Place an order | Yes | No | Yes | No |
| Update order status | Yes | Own restaurant only | No | No |
| Write a review | No | No | Yes | No |
| Manage users | Yes | No | No | No |

## Docker Commands

```bash
docker-compose up --build          # start
docker-compose up --build -d       # start in background
docker-compose exec api alembic upgrade head   # run migrations
docker-compose logs api            # view logs
docker-compose down                # stop
docker-compose down -v             # stop and wipe data
```

Built by Anjil Timsina
