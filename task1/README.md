# Minimalistic Online Shop Backend

A minimal FastAPI backend for an online shop with SQLite persistence and full CRUD for Customer, ShopItemCategory, ShopItem, and Order. Includes endpoint tests using Pytest.

## Project Structure

```
app/
  main.py
tests/
  test_endpoints.py
README.md
```

## Setup

1. **Install dependencies**  
   Python 3.8+ required.
   ```sh
   pip install fastapi sqlalchemy pydantic uvicorn pytest pydantic[email
   ```
2. **For tets**  
   Python 3.8+ required.
   ```sh
   pip install httpx
   ```

2. **Run the application**
   ```sh
   uvicorn app.main:app --reload
   ```
   The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

3. **Run the tests**
   ```sh
   PYTHONPATH=$PYTHONPATH:. pytest tests
   ```

## Notes

- The database (`shop.db`) is created automatically in the project root.
- Initial test data is inserted on first run.
- API docs available at `/docs` when the server is running.
~~~