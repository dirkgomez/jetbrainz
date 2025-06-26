# Online Shop Backend API

A minimalistic backend web application for an online shop built with FastAPI, SQLite, and pytest.

## Features

- Full CRUD APIs for:
  - Customer management
  - Shop Item Categories
  - Shop Items
  - Orders and Order Items
- SQLite database with automatic initialization
- Comprehensive test coverage with pytest
- Pre-loaded test data

## Project Structure

```
task1/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration and session management
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic schemas for request/response
│   ├── crud.py              # CRUD operations
│   └── routers/
│       ├── __init__.py
│       ├── customers.py     # Customer endpoints
│       ├── categories.py    # ShopItemCategory endpoints
│       ├── items.py         # ShopItem endpoints
│       └── orders.py        # Order endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configuration and fixtures
│   ├── test_customers.py    # Customer API tests
│   ├── test_categories.py   # Category API tests
│   ├── test_items.py        # Shop Item API tests
│   └── test_orders.py       # Order API tests
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone or download this project
2. Navigate to the project directory:
   ```bash
   cd task1
   ```

3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. The API will be available at: `http://localhost:8000`

3. Access the interactive API documentation at: `http://localhost:8000/docs`

4. Access the alternative API documentation at: `http://localhost:8000/redoc`

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app
```

Run tests with verbose output:
```bash
pytest -v
```

Run specific test file:
```bash
pytest tests/test_customers.py
```

## API Endpoints

### Customers
- `GET /customers/` - List all customers
- `POST /customers/` - Create a new customer
- `GET /customers/{customer_id}` - Get customer by ID
- `PUT /customers/{customer_id}` - Update customer
- `DELETE /customers/{customer_id}` - Delete customer

### Shop Item Categories
- `GET /categories/` - List all categories
- `POST /categories/` - Create a new category
- `GET /categories/{category_id}` - Get category by ID
- `PUT /categories/{category_id}` - Update category
- `DELETE /categories/{category_id}` - Delete category

### Shop Items
- `GET /items/` - List all shop items
- `POST /items/` - Create a new shop item
- `GET /items/{item_id}` - Get shop item by ID
- `PUT /items/{item_id}` - Update shop item
- `DELETE /items/{item_id}` - Delete shop item

### Orders
- `GET /orders/` - List all orders
- `POST /orders/` - Create a new order
- `GET /orders/{order_id}` - Get order by ID
- `PUT /orders/{order_id}` - Update order
- `DELETE /orders/{order_id}` - Delete order

## Database

The application uses SQLite as the database backend. The database file (`shop.db`) will be created automatically when you first run the application. The database is initialized with sample data for testing purposes.

## Testing

The test suite includes:
- Unit tests for all CRUD operations
- Integration tests for API endpoints
- Test data fixtures for consistent testing
- Cleanup procedures to maintain test isolation

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight, file-based database
- **Pydantic**: Data validation using Python type annotations
- **pytest**: Testing framework
- **Uvicorn**: ASGI server for running the application
