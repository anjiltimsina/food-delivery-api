# 🍔 Food Delivery API

A production-level Food Delivery backend REST API built with FastAPI, PostgreSQL, and SQLAlchemy.

## Tech Stack
- **FastAPI** — Web framework
- **PostgreSQL** — Database
- **SQLAlchemy** — ORM (async)
- **Alembic** — Database migrations
- **JWT** — Authentication
- **Passlib/Bcrypt** — Password hashing

## Features
- JWT Authentication with access/refresh tokens
- Role based access control (Admin, Customer, Restaurant Owner, Delivery Rider)
- Restaurant management with admin approval system
- Food items management
- Cart system
- Order management
- Reviews system

## Project Structure
\`\`\`
FoodDeliveryAPI/
├── app/
│   ├── core/          # Config, security, dependencies
│   ├── db/            # Database connection
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── routers/       # API endpoints
│   ├── services/      # Business logic
│   └── main.py
├── migrations/        # Alembic migrations
├── .env.example
├── requirements.txt
└── README.md
\`\`\`

## Setup Instructions

### 1. Clone the repo
\`\`\`bash
git clone https://github.com/yourusername/food-delivery-api.git
cd food-delivery-api
\`\`\`

### 2. Create virtual environment
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
\`\`\`

### 3. Install dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Setup environment variables
\`\`\`bash
cp .env.example .env
# Edit .env with your actual values
\`\`\`

### 5. Run migrations
\`\`\`bash
alembic upgrade head
\`\`\`

### 6. Start the server
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

### 7. Open API docs
\`\`\`
http://localhost:8000/docs
\`\`\`

## API Endpoints

### Auth
| Method | Endpoint | Access |
|--------|----------|--------|
| POST | /auth/register | Public |
| POST | /auth/login | Public |
| POST | /auth/refresh | Public |
| GET | /auth/me | Authenticated |

### Users
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | /users/ | Admin |
| GET | /users/{id} | Admin |
| PUT | /users/{id} | Admin/Owner |
| PATCH | /users/{id}/deactivate | Admin |
| PATCH | /users/{id}/activate | Admin |

### Restaurants
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | /restaurants/ | Public |
| POST | /restaurants/ | Restaurant Owner |
| PUT | /restaurants/{id} | Owner/Admin |
| PATCH | /restaurants/{id}/approve | Admin |
| DELETE | /restaurants/{id} | Owner/Admin |

### Food Items
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | /restaurants/{id}/foods | Public |
| POST | /restaurants/{id}/foods | Owner/Admin |
| PUT | /restaurants/{id}/foods/{id} | Owner/Admin |
| DELETE | /restaurants/{id}/foods/{id} | Owner/Admin |

### Cart
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | /cart/ | Customer |
| POST | /cart/items | Customer |
| PATCH | /cart/items/{id} | Customer |
| DELETE | /cart/items/{id} | Customer |
| DELETE | /cart/ | Customer |