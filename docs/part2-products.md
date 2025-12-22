# Part 2: FastAPI Deep Dive with Pydantic

## Objective
Build a complete FastAPI application covering all Module 3 topics: routes, path parameters, query parameters, request body with Pydantic models, and JSON responses.

---

## 1. Introduction to Pydantic Models

### What is Pydantic?
- Data validation library using Python type hints
- Automatically validates incoming data
- Provides clear error messages
- Converts data to correct types

### Why Use Pydantic with FastAPI?
- **Automatic validation**: FastAPI validates request data automatically
- **Clear errors**: Users get detailed error messages
- **Documentation**: Models appear in interactive docs
- **Type safety**: Catch errors during development

### Basic Pydantic Model

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_available: bool = True
    description: str = None
```

**Key Points:**
- Inherit from `BaseModel`
- Use type hints for fields
- Set default values with `=`
- `None` means optional field

---

## 2. Complete Example: Product Management API

We'll build a Product Management API that demonstrates all Module 3 concepts.

### Create `product_api.py`

# UPDATE PRODUCT (PUT with path parameter and request body)
@app.put("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def update_product(
    product_id: int = Path(..., gt=0, description="The ID of the product to update"),
    product_update: ProductUpdate = None
):
    if product_id not in products_db:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found"
        )

    existing_product = products_db[product_id]

    # Update only provided fields
    update_data = product_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        existing_product[field] = value

    products_db[product_id] = existing_product

    return existing_product

# DELETE PRODUCT
@app.delete("/products/{product_id}", tags=["Products"])
def delete_product(
    product_id: int = Path(..., gt=0, description="The ID of the product to delete")
):
    if product_id not in products_db:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found"
        )

    deleted_product = products_db.pop(product_id)

    return {
        "message": "Product deleted successfully",
        "deleted_product": deleted_product
    }

# SEARCH PRODUCTS (combining path and query parameters)
@app.get("/categories/{category}/products", response_model=List[ProductResponse], tags=["Search"])
def search_by_category(
    category: str = Path(..., description="Category to search in"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    in_stock: bool = Query(True, description="Show only in-stock items")
):
    filtered = [
        p for p in products_db.values()
        if p["category"].lower() == category.lower() and p["in_stock"] == in_stock
    ]

    if min_price is not None:
        filtered = [p for p in filtered if p["price"] >= min_price]

    if max_price is not None:
        filtered = [p for p in filtered if p["price"] <= max_price]

    return filtered

# STATISTICS ENDPOINT
@app.get("/stats", tags=["Statistics"])
def get_statistics():
    if not products_db:
        return {"message": "No products available"}

    prices = [p["price"] for p in products_db.values()]
    categories = {}
    in_stock_count = sum(1 for p in products_db.values() if p["in_stock"])

    for product in products_db.values():
        cat = product["category"]
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "total_products": len(products_db),
        "in_stock": in_stock_count,
        "out_of_stock": len(products_db) - in_stock_count,
        "average_price": sum(prices) / len(prices),
        "min_price": min(prices),
        "max_price": max(prices),
        "categories": categories
    }
```

---

## 3. Testing the Complete API (Hands-on)

### Step 1: Run the Application

```bash
uvicorn product_api:app --reload
```

### Step 2: Open Swagger UI

Navigate to: http://127.0.0.1:8000/docs

### Step 3: Test Each Endpoint

**1. Create Products (POST /products)**

Test with these JSON bodies:

```json
{
  "name": "Laptop",
  "price": 1200.00,
  "category": "Electronics",
  "in_stock": true,
  "description": "High-performance laptop"
}
```

```json
{
  "name": "Office Chair",
  "price": 250.00,
  "category": "Furniture",
  "in_stock": true,
  "description": "Ergonomic office chair"
}
```

```json
{
  "name": "Smartphone",
  "price": 800.00,
  "category": "Electronics",
  "in_stock": false,
  "description": "Latest smartphone model"
}
```

**2. Get All Products (GET /products)**
- Try without parameters
- Try with category=Electronics
- Try with min_price=500 and max_price=1000
- Try with in_stock=true

**3. Get Single Product (GET /products/1)**
- Get product with ID 1
- Try with non-existent ID (e.g., 999) to see error handling

**4. Update Product (PUT /products/1)**

```json
{
  "price": 1100.00,
  "in_stock": false
}
```

**5. Search by Category (GET /categories/Electronics/products)**
- Try with in_stock=true
- Try with min_price=500

**6. Get Statistics (GET /stats)**

**7. Delete Product (DELETE /products/2)**

---

## 4. Key Concepts Covered

### Defining Routes
```python
@app.get("/products")      # GET method
@app.post("/products")     # POST method
@app.put("/products/{id}") # PUT method
@app.delete("/products/{id}") # DELETE method
```

### Path Parameters
```python
@app.get("/products/{product_id}")
def get_product(product_id: int = Path(..., gt=0)):
    pass
```

### Query Parameters
```python
@app.get("/products")
def get_products(
    category: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    pass
```

### Request Body with Pydantic
```python
class Product(BaseModel):
    name: str
    price: float

@app.post("/products")
def create_product(product: Product):
    pass
```

### Response Models
```python
@app.get("/products", response_model=List[ProductResponse])
def get_products():
    pass
```

### Validation with Field
```python
from pydantic import Field

class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
```

---

## 5. Common Patterns and Best Practices

### Error Handling
```python
from fastapi import HTTPException

if product_id not in products_db:
    raise HTTPException(status_code=404, detail="Product not found")
```

### Optional Fields
```python
from typing import Optional

description: Optional[str] = None
```

### Default Values
```python
in_stock: bool = True
skip: int = Query(0)
```

### Validation Constraints
- gt: greater than
- ge: greater than or equal
- lt: less than
- le: less than or equal
- min_length: minimum string length
- max_length: maximum string length

---

## Quick Reference Card

| Concept | Syntax | Example |
|---------|--------|---------|
| Path Parameter | {param} | /users/{user_id} |
| Query Parameter | param: type = Query() | skip: int = Query(0) |
| Request Body | param: Model | product: Product |
| Optional Field | Optional[type] | Optional[str] |
| Default Value | param = value | skip = 0 |
| Validation | Field(...) | Field(gt=0) |
| HTTP Exception | HTTPException() | HTTPException(404) |

---

## Summary

You have now learned:
- How to use Pydantic models for data validation
- All HTTP methods (GET, POST, PUT, DELETE)
- Path parameters with validation
- Query parameters with filtering
- Request body handling
- Response models
- Error handling with HTTPException

**Next**: Part 3 - Hands-on exercise combining FastAPI with Pandas!
