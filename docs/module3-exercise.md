# Module 3: FastAPI Exercise - Library Management System

## Objective
Build a complete Library Management API using FastAPI that manages books. This exercise will help you practice all Module 3 concepts:
- GET, POST, PUT, DELETE routes
- Path parameters
- Query parameters
- Pydantic models for validation
- JSON responses
- Error handling

**Time Estimate:** 2-3 hours

---

## Requirements

### What You'll Build
A Library Management API that can:
1. List all books (with filtering)
2. Get a specific book by ID
3. Add new books
4. Update book information
5. Delete books
6. Search books by author
7. Get library statistics

---

## Part 1: Setup (15 minutes)

### 1.1 Create the File
Create a new file named `library_api.py` in your workspace.

### 1.2 Import Required Libraries
```python
from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
```

### 1.3 Initialize FastAPI
```python
app = FastAPI(
    title="Library Management API",
    description="API for managing library books",
    version="1.0.0"
)
```

### 1.4 Create In-Memory Database
```python
# In-memory database
books_db = {}
book_counter = 0
```

---

## Part 2: Define Pydantic Models (20 minutes)

### 2.1 Create Book Model
Create a `Book` model with the following fields:
- `title` (str, required, 1-200 characters)
- `author` (str, required, 1-100 characters)
- `isbn` (str, required, exactly 13 characters)
- `published_year` (int, required, between 1000 and 2100)
- `pages` (int, required, greater than 0)
- `available` (bool, default True)
- `genre` (str, required)
- `summary` (str, optional, max 1000 characters)

**Hint:** Use `Field()` for validation rules.

Add a `Config` class with an example:
```python
class Config:
    json_schema_extra = {
        "example": {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "isbn": "9780743273565",
            "published_year": 1925,
            "pages": 180,
            "available": True,
            "genre": "Fiction",
            "summary": "A classic American novel set in the 1920s"
        }
    }
```

### 2.2 Create BookUpdate Model
Create a model for updating books where all fields are optional.

### 2.3 Create BookResponse Model
Create a response model that includes all book fields plus:
- `id` (int)
- `added_at` (str) - timestamp when book was added

---

## Part 3: Implement API Endpoints (90 minutes)

### 3.1 Root Endpoint (5 minutes)
**Route:** `GET /`

Return a welcome message with:
- API name
- Link to docs (`/docs`)
- Total number of books

### 3.2 Get All Books (20 minutes)
**Route:** `GET /books`

**Query Parameters:**
- `genre` (optional) - filter by genre
- `author` (optional) - filter by author (case-insensitive)
- `available` (optional, bool) - filter by availability
- `min_pages` (optional, int >= 0) - minimum number of pages
- `max_pages` (optional, int >= 0) - maximum number of pages
- `skip` (default 0, >= 0) - pagination offset
- `limit` (default 10, between 1-100) - max items to return

**Response:** List of `BookResponse`

**Implementation Steps:**
1. Start with all books from `books_db`
2. Filter by genre if provided
3. Filter by author if provided (case-insensitive match)
4. Filter by availability if provided
5. Filter by page range if provided
6. Apply pagination (skip and limit)
7. Return filtered list

### 3.3 Get Single Book (10 minutes)
**Route:** `GET /books/{book_id}`

**Path Parameter:**
- `book_id` (int, > 0) - The ID of the book

**Response:** `BookResponse`

**Error Handling:**
- Return 404 if book not found

### 3.4 Create Book (15 minutes)
**Route:** `POST /books`

**Request Body:** `Book` model

**Response:** `BookResponse` (status code 201)

**Implementation:**
1. Increment `book_counter`
2. Create book data dictionary with all fields
3. Add `id` and `added_at` (use `datetime.now().isoformat()`)
4. Store in `books_db`
5. Return the created book

### 3.5 Update Book (15 minutes)
**Route:** `PUT /books/{book_id}`

**Path Parameter:**
- `book_id` (int, > 0)

**Request Body:** `BookUpdate` model

**Response:** `BookResponse`

**Error Handling:**
- Return 404 if book not found

**Implementation:**
1. Check if book exists
2. Get update data (only fields that were provided)
3. Update existing book fields
4. Return updated book

**Hint:** Use `.model_dump(exclude_unset=True)` to get only provided fields.

### 3.6 Delete Book (10 minutes)
**Route:** `DELETE /books/{book_id}`

**Path Parameter:**
- `book_id` (int, > 0)

**Response:** JSON with success message and deleted book info

**Error Handling:**
- Return 404 if book not found

### 3.7 Search by Author (15 minutes)
**Route:** `GET /authors/{author_name}/books`

**Path Parameter:**
- `author_name` (str) - Author to search for

**Query Parameters:**
- `available` (optional, bool) - filter by availability
- `genre` (optional, str) - filter by genre

**Response:** List of `BookResponse`

**Implementation:**
Filter books by author name (case-insensitive), then apply additional filters.

### 3.8 Library Statistics (20 minutes)
**Route:** `GET /stats`

**Response:** JSON with statistics:
```json
{
    "total_books": 0,
    "available_books": 0,
    "borrowed_books": 0,
    "total_pages": 0,
    "average_pages": 0,
    "genres": {},
    "authors": {}
}
```

**Implementation:**
1. Count total books
2. Count available vs borrowed
3. Calculate total and average pages
4. Count books per genre (dictionary)
5. Count books per author (dictionary)
6. Handle empty database case

---

## Part 4: Load Sample Data (15 minutes)

### 4.1 Create Sample JSON File
Create a file named `library_data.json` with sample books:

```json
[
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "isbn": "9780061120084",
        "published_year": 1960,
        "pages": 324,
        "available": true,
        "genre": "Fiction",
        "summary": "A gripping tale of racial injustice and childhood innocence"
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "isbn": "9780451524935",
        "published_year": 1949,
        "pages": 328,
        "available": true,
        "genre": "Science Fiction",
        "summary": "A dystopian social science fiction novel"
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "isbn": "9780141439518",
        "published_year": 1813,
        "pages": 432,
        "available": false,
        "genre": "Romance",
        "summary": "A romantic novel of manners"
    },
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "9780743273565",
        "published_year": 1925,
        "pages": 180,
        "available": true,
        "genre": "Fiction",
        "summary": "A classic American novel set in the 1920s"
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "isbn": "9780547928227",
        "published_year": 1937,
        "pages": 310,
        "available": true,
        "genre": "Fantasy",
        "summary": "A fantasy adventure novel"
    },
    {
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "isbn": "9780439708180",
        "published_year": 1997,
        "pages": 309,
        "available": false,
        "genre": "Fantasy",
        "summary": "The first book in the Harry Potter series"
    },
    {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "isbn": "9780316769488",
        "published_year": 1951,
        "pages": 277,
        "available": true,
        "genre": "Fiction",
        "summary": "A story about teenage rebellion and alienation"
    },
    {
        "title": "Animal Farm",
        "author": "George Orwell",
        "isbn": "9780451526342",
        "published_year": 1945,
        "pages": 112,
        "available": true,
        "genre": "Fiction",
        "summary": "An allegorical novella about Soviet totalitarianism"
    }
]
```

### 4.2 Create Data Loader Function
Add this function to load data into your API:

```python
import json

def load_sample_data():
    """Load sample books from JSON file into database"""
    global book_counter
    
    try:
        with open("library_data.json", "r") as f:
            books = json.load(f)
        
        for book_data in books:
            book_counter += 1
            book_entry = {
                "id": book_counter,
                "added_at": datetime.now().isoformat(),
                **book_data
            }
            books_db[book_counter] = book_entry
        
        print(f"✓ Loaded {len(books)} sample books")
        
    except FileNotFoundError:
        print("⚠ library_data.json not found - starting with empty database")
    except json.JSONDecodeError:
        print("⚠ Error reading library_data.json - invalid JSON format")
```

### 4.3 Add Startup Event
Add this code after your endpoint definitions:

```python
@app.on_event("startup")
def startup_event():
    """Load sample data when API starts"""
    load_sample_data()
```

---

## Part 5: Testing (30 minutes)

### 5.1 Run the API
```bash
uvicorn library_api:app --reload
```

### 5.2 Test with Interactive Docs
Open http://127.0.0.1:8000/docs

### 5.3 Test Checklist

**Basic Operations:**
- ✅ GET / - Check welcome message shows total books
- ✅ GET /books - Should return 8 books
- ✅ GET /books/1 - Get first book
- ✅ GET /books/999 - Should return 404

**Filtering:**
- ✅ GET /books?genre=Fiction - Should return 4 books
- ✅ GET /books?author=George%20Orwell - Should return 2 books
- ✅ GET /books?available=true - Should return 6 books
- ✅ GET /books?min_pages=300 - Books with 300+ pages
- ✅ GET /books?max_pages=200 - Books with ≤ 200 pages

**Pagination:**
- ✅ GET /books?skip=0&limit=3 - First 3 books
- ✅ GET /books?skip=3&limit=3 - Next 3 books

**Create:**
- ✅ POST /books - Add a new book:
```json
{
    "title": "The Alchemist",
    "author": "Paulo Coelho",
    "isbn": "9780062315007",
    "published_year": 1988,
    "pages": 208,
    "available": true,
    "genre": "Fiction",
    "summary": "A philosophical book about following your dreams"
}
```

**Update:**
- ✅ PUT /books/1 - Update book availability:
```json
{
    "available": false
}
```

**Delete:**
- ✅ DELETE /books/1 - Delete a book
- ✅ GET /books/1 - Verify it's gone (404)

**Search:**
- ✅ GET /authors/George%20Orwell/books - Should return 2 books
- ✅ GET /authors/Jane%20Austen/books?available=false

**Statistics:**
- ✅ GET /stats - Check all statistics are calculated correctly

---

## Part 6: Validation Testing (10 minutes)

Test that Pydantic validation works correctly:

### Invalid Data Tests:

**Empty title:**
```json
{
    "title": "",
    "author": "Test Author",
    "isbn": "1234567890123",
    "published_year": 2020,
    "pages": 100,
    "genre": "Fiction"
}
```
❌ Should fail with validation error

**Negative pages:**
```json
{
    "title": "Test Book",
    "author": "Test Author",
    "isbn": "1234567890123",
    "published_year": 2020,
    "pages": -100,
    "genre": "Fiction"
}
```
❌ Should fail with validation error

**Invalid year:**
```json
{
    "title": "Test Book",
    "author": "Test Author",
    "isbn": "1234567890123",
    "published_year": 3000,
    "pages": 100,
    "genre": "Fiction"
}
```
❌ Should fail with validation error

**Wrong ISBN length:**
```json
{
    "title": "Test Book",
    "author": "Test Author",
    "isbn": "123",
    "published_year": 2020,
    "pages": 100,
    "genre": "Fiction"
}
```
❌ Should fail with validation error

---

## Success Criteria

You've successfully completed the exercise when:

1. ✅ All 8 endpoints are implemented
2. ✅ Sample data loads automatically on startup
3. ✅ All filters work correctly
4. ✅ Pagination works as expected
5. ✅ Validation rejects invalid data
6. ✅ Error handling returns appropriate 404 responses
7. ✅ Statistics endpoint calculates correctly
8. ✅ Interactive docs at /docs show all endpoints

---

## Bonus Challenges (Optional)

If you finish early, try these enhancements:

### Bonus 1: Partial Title Search
Add a query parameter to `GET /books` for partial title search:
```python
title_search: str | None = Query(None, description="Search in book titles")
```

### Bonus 2: Sort Options
Add sorting to `GET /books`:
```python
sort_by: str = Query("id", description="Sort by: id, title, author, year, pages")
order: str = Query("asc", description="Order: asc or desc")
```

### Bonus 3: Year Range Filter
Add year range filtering:
```python
from_year: int | None = Query(None, ge=1000)
to_year: int | None = Query(None, le=2100)
```

### Bonus 4: Checkout/Return System
Add endpoints to checkout and return books:
- `POST /books/{book_id}/checkout` - Mark as unavailable
- `POST /books/{book_id}/return` - Mark as available

---

## Tips for Success

1. **Build incrementally** - Implement one endpoint at a time and test it
2. **Use the docs** - FastAPI's /docs is your best friend for testing
3. **Copy patterns** - Look at `products_api.py` for reference
4. **Read errors carefully** - Pydantic gives detailed error messages
5. **Test as you go** - Don't wait until the end to test
6. **Use print statements** - Debug by printing variables
7. **Check data types** - Make sure you're comparing the right types (e.g., lowercase strings)

---

## Common Mistakes to Avoid

❌ Forgetting `global book_counter` in POST endpoint  
❌ Not handling case-insensitive searches for author/genre  
❌ Forgetting to check if book exists before update/delete  
❌ Not using `exclude_unset=True` when updating  
❌ Incorrect Field validation (check gt vs ge, min_length vs max_length)  
❌ Forgetting to return appropriate status codes (201 for creation)  
❌ Not handling empty database in statistics endpoint  

---

## Expected Output Examples

### GET /stats (with sample data)
```json
{
    "total_books": 8,
    "available_books": 6,
    "borrowed_books": 2,
    "total_pages": 2272,
    "average_pages": 284,
    "genres": {
        "Fiction": 4,
        "Science Fiction": 1,
        "Romance": 1,
        "Fantasy": 2
    },
    "authors": {
        "Harper Lee": 1,
        "George Orwell": 2,
        "Jane Austen": 1,
        "F. Scott Fitzgerald": 1,
        "J.R.R. Tolkien": 1,
        "J.K. Rowling": 1,
        "J.D. Salinger": 1
    }
}
```

### GET /books?genre=Fantasy
```json
[
    {
        "id": 5,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "isbn": "9780547928227",
        "published_year": 1937,
        "pages": 310,
        "available": true,
        "genre": "Fantasy",
        "summary": "A fantasy adventure novel",
        "added_at": "2024-01-15T10:30:00"
    },
    {
        "id": 6,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "isbn": "9780439708180",
        "published_year": 1997,
        "pages": 309,
        "available": false,
        "genre": "Fantasy",
        "summary": "The first book in the Harry Potter series",
        "added_at": "2024-01-15T10:30:01"
    }
]
```

---

## Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Pydantic Docs:** https://docs.pydantic.dev/
- **Reference:** Your `products_api.py` file
- **Training Material:** `docs/part2-products.md`

---

**Good luck! Take your time and enjoy building your Library Management API! 📚**
