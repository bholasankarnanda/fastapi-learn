from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="Product Management API",
    description="API for managing products with FastAPI",
    version="1.0.0",
)

# PYDANTIC MODELS (Data Validation)


class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(default=True, description="Stock availability")
    description: str | None = Field(
        None, max_length=500, description="Product description (optional)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "price": 999.99,
                "category": "Electronics",
                "in_stock": True,
                "description": "High-performance laptop",
            }
        }


class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    price: float | None = Field(None, gt=0)
    category: str | None = None
    in_stock: bool | None = None
    description: str | None = Field(None, max_length=500)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str
    in_stock: bool
    description: str | None
    created_at: str


# IN-MEMORY DATABASE (Simulated)
products_db = {}
product_counter = 0

# API ENDPOINTS


# ROOT ENDPOINT
@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to Product Management API",
        "docs": "/docs",
        "total_products": len(products_db),
    }


# GET ALL PRODUCTS (with query parameters for filtering)
@app.get("/products", response_model=List[ProductResponse], tags=["Products"])
def get_all_products(
    category: str | None = Query(None, description="Filter by category"),
    min_price: float | None = Query(None, ge=0, description="Minimum price"),
    max_price: float | None = Query(None, ge=0, description="Maximum price"),
    in_stock: bool | None = Query(None, description="Filter by stock availability"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
):
    filtered_products = list(products_db.values())

    # Apply filters
    if category:
        filtered_products = [
            p for p in filtered_products if p["category"].lower() == category.lower()
        ]

    if min_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] >= min_price]

    if max_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] <= max_price]

    if in_stock is not None:
        filtered_products = [p for p in filtered_products if p["in_stock"] == in_stock]

    # Apply pagination
    paginated_products = filtered_products[skip : skip + limit]

    return paginated_products


# GET SINGLE PRODUCT (path parameter)
@app.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def get_product(
    product_id: int = Path(..., gt=0, description="The ID of the product to retrieve")
):
    if product_id not in products_db:
        raise HTTPException(
            status_code=404, detail=f"Product with ID {product_id} not found"
        )

    return products_db[product_id]


# CREATE PRODUCT (POST with request body)
@app.post(
    "/products", response_model=ProductResponse, status_code=201, tags=["Products"]
)
def create_product(product: Product):
    global product_counter
    product_counter += 1

    product_data = {
        "id": product_counter,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "in_stock": product.in_stock,
        "description": product.description,
        "created_at": datetime.now().isoformat(),
    }

    products_db[product_counter] = product_data

    return product_data


# UPDATE PRODUCT (PUT with path parameter and request body)
@app.put("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def update_product(
    product_id: int = Path(..., gt=0, description="The ID of the product to update"),
    product_update: ProductUpdate = None,
):
    if product_id not in products_db:
        raise HTTPException(
            status_code=404, detail=f"Product with ID {product_id} not found"
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
            status_code=404, detail=f"Product with ID {product_id} not found"
        )

    deleted_product = products_db.pop(product_id)

    return {
        "message": "Product deleted successfully",
        "deleted_product": deleted_product,
    }


# SEARCH PRODUCTS (combining path and query parameters)
@app.get(
    "/categories/{category}/products",
    response_model=List[ProductResponse],
    tags=["Search"],
)
def search_by_category(
    category: str = Path(..., description="Category to search in"),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    in_stock: bool = Query(True, description="Show only in-stock items"),
):
    print(category)
    filtered = [
        p
        for p in products_db.values()
        if p["category"].lower() == category.lower() and p["in_stock"] == in_stock
    ]
    for p in filtered:
        print(p)

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
        "categories": categories,
    }


@app.on_event("startup")
def startup_event():
    print("Starting up...")
    pass
