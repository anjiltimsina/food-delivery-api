# 🍔 Food Delivery API

A production-level Food Delivery backend REST API built with FastAPI, PostgreSQL, and SQLAlchemy.

## Tech Stack
- **FastAPI** — Web framework
- **PostgreSQL** — Database
- **SQLAlchemy** — ORM (async)
- **Alembic** — Database migrations
- **JWT** — Authentication
- **Passlib/Bcrypt** — Password hashing
- **Google OAuth** — Social login
- **Cloudinary** — Image uploads (production)
- **Docker** — Containerization
- **SlowAPI** — Rate limiting

## Features
- JWT Authentication with access/refresh tokens
- Google OAuth login
- Role based access control (Admin, Customer, Restaurant Owner, Delivery Rider)
- Restaurant management with admin approval system
- Food items management with image upload
- Cart system
- Order management with status tracking
- Reviews system with auto rating update
- Pagination on all list endpoints
- Rate limiting on auth endpoints
- Request logging middleware
- CORS middleware
- Dockerized for easy deployment

## Project Structure
\`\`\`
FoodDeliveryAPI/
├── app/
│   ├── core/
│   │   ├── config.py          # Environment variables
│   │   ├── security.py        # JWT, hashing
│   │   └── dependencies.py    # Route guards, role checks
│   ├── db/
│   │   ├── database.py        # Async DB connection
│   │   └── base.py            # Base model
│   ├── models/                # SQLAlchemy models
│   │   ├── user.py
│   │   ├── restaurant.py
│   │   ├── food_item.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── review.py
│   ├── schemas/               # Pydantic validation
│   │   ├── user.py
│   │   ├── restaurant.py
│   │   ├── food_item.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   ├── review.py
│   │   └── pagination.py
│   ├── routers/               # API endpoints
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── restaurants.py
│   │   ├── food_items.py
│   │   ├── cart.py
│   │   ├── orders.py
│   │   └── reviews.py
│   ├── services/              # Business logic
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── restaurant_service.py
│   │   ├── food_item_service.py
│   │   ├── cart_service.py
│   │   ├── order_service.py
│   │   ├── review_service.py
│   │   └── google_auth_service.py
│   ├── middleware/
│   │   ├── auth_middleware.py
│   │   ├── logging_middleware.py
│   │   └── rate_limit_middleware.py
│   ├── utils/
│   │   ├── upload.py          # Image uploads
│   │   └── pagination.py      # Pagination helper
│   └── main.py
├── migrations/                # Alembic migrations
├── tests/
│   ├── test_auth.py
│   ├── test_restaurants.py
│   ├── test_orders.py
│   └── test_cart.py
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
\`\`\`

---

## Setup Instructions

### Option 1 — Run with Docker (Recommended)

#### 1. Clone the repo
\`\`\`bash
git clone https://github.com/yourusername/food-delivery-api.git
cd food-delivery-api
\`\`\`

#### 2. Setup environment variables
\`\`\`bash
cp .env.example .env
# Edit .env with your actual values
\`\`\`

#### 3. Start with Docker
\`\`\`bash
docker-compose up --build
\`\`\`

#### 4. Run migrations
\`\`\`bash
docker-compose exec api alembic upgrade head
\`\`\`

#### 5. Open API docs
\`\`\`
http://localhost:8001/docs
\`\`\`

---

### Option 2 — Run Locally

#### 1. Clone the repo
\`\`\`bash
git clone https://github.com/yourusername/food-delivery-api.git
cd food-delivery-api
\`\`\`

#### 2. Create virtual environment
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
\`\`\`

#### 3. Install dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

#### 4. Setup environment variables
\`\`\`bash
cp .env.example .env
# Edit .env with your actual values
\`\`\`

#### 5. Make sure PostgreSQL is running then run migrations
\`\`\`bash
alembic upgrade head
\`\`\`

#### 6. Start the server
\`\`\`bash
uvicorn app.main:app --reload --port 8001
\`\`\`

#### 7. Open API docs
\`\`\`
http://localhost:8001/docs
\`\`\`

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values:

\`\`\`ini
APP_NAME="FoodDeliveryAPI"
DEBUG=True
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Local development
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/food_delivery_db

# Docker
# DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/food_delivery_db

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8001/auth/google/callback

# Cloudinary (for production image uploads)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
\`\`\`

---

## API Endpoints

### Auth
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | /auth/register | Public | Register new user |
| POST | /auth/login | Public | Login with email/password |
| POST | /auth/refresh | Public | Refresh access token |
| GET | /auth/me | Authenticated | Get current user |
| GET | /auth/google/login | Public | Login with Google |
| GET | /auth/google/callback | Public | Google OAuth callback |

### Users
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | /users/ | Admin | Get all users (paginated) |
| GET | /users/{id} | Admin | Get user by id |
| PUT | /users/{id} | Admin/Owner | Update user |
| POST | /users/me/upload-image | Authenticated | Upload profile image |
| PATCH | /users/me/deactivate | Authenticated | Deactivate own account |
| PATCH | /users/{id}/deactivate | Admin | Deactivate any user |
| PATCH | /users/{id}/activate | Admin | Activate user |

### Restaurants
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | /restaurants/ | Public | Get approved restaurants (paginated) |
| GET | /restaurants/admin/all | Admin | Get all restaurants (paginated) |
| GET | /restaurants/{id} | Public | Get single restaurant |
| POST | /restaurants/ | Restaurant Owner | Create restaurant |
| PUT | /restaurants/{id} | Owner/Admin | Update restaurant |
| POST | /restaurants/{id}/upload-image | Owner/Admin | Upload restaurant image |
| PATCH | /restaurants/{id}/approve | Admin | Approve restaurant |
| DELETE | /restaurants/{id} | Owner/Admin | Delete restaurant |

### Food Items
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | /restaurants/{id}/foods | Public | Get food items (paginated) |
| GET | /restaurants/{id}/foods/{fid} | Public | Get single food item |
| POST | /restaurants/{id}/foods | Owner/Admin | Add food item |
| PUT | /restaurants/{id}/foods/{fid} | Owner/Admin | Update food item |
| POST | /restaurants/{id}/foods/{fid}/upload-image | Owner/Admin | Upload food image |
| DELETE | /restaurants/{id}/foods/{fid} | Owner/Admin | Delete food item |

### Cart
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | /cart/ | Customer | View cart |
| POST | /cart/items | Customer | Add item to cart |
| PATCH | /cart/items/{id} | Customer | Update item quantity |
| DELETE | /cart/items/{id} | Customer | Remove item |
| DELETE | /cart/ | Customer | Clear cart |

### Orders
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | /orders/ | Customer | Place order from cart |
| GET | /orders/my | Customer | Get my orders (paginated) |
| GET | /orders/all | Admin | Get all orders (paginated) |
| GET | /orders/restaurant/{id} | Owner/Admin | Get restaurant orders (paginated) |
| GET | /orders/{id} | Authenticated | Get single order |
| PATCH | /orders/{id}/status | Owner/Admin | Update order status |
| PATCH | /orders/{id}/cancel | Authenticated | Cancel order |

### Reviews
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | /reviews/restaurant/{id} | Public | Get restaurant reviews (paginated) |
| GET | /reviews/my | Customer | Get my reviews (paginated) |
| POST | /reviews/ | Customer | Create review |
| DELETE | /reviews/{id} | Admin/Owner | Delete review |

---

## Order Status Flow
\`\`\`
PENDING → CONFIRMED → PREPARING → OUT_FOR_DELIVERY → DELIVERED
                                                    ↘ CANCELLED
\`\`\`

---

## Role Permissions

| Feature | Admin | Restaurant Owner | Customer | Public |
|---------|-------|-----------------|----------|--------|
| View restaurants | ✅ | ✅ | ✅ | ✅ |
| Create restaurant | ✅ | ✅ | ❌ | ❌ |
| Approve restaurant | ✅ | ❌ | ❌ | ❌ |
| Manage food items | ✅ | ✅ (own) | ❌ | ❌ |
| Place orders | ✅ | ❌ | ✅ | ❌ |
| View all orders | ✅ | ❌ | ❌ | ❌ |
| Update order status | ✅ | ✅ (own) | ❌ | ❌ |
| Write reviews | ❌ | ❌ | ✅ | ❌ |
| Manage users | ✅ | ❌ | ❌ | ❌ |

---

## Running Tests
\`\`\`bash
pytest tests/ -v
\`\`\`

---

## Docker Commands
\`\`\`bash
# Start everything
docker-compose up --build

# Run in background
docker-compose up --build -d

# Run migrations
docker-compose exec api alembic upgrade head

# View logs
docker-compose logs api

# Stop everything
docker-compose down

# Stop and delete all data
docker-compose down -v
\`\`\`

---

Built By : Anjil Timsina