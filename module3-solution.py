from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="Library Management API",
    description="API for managing library books",
    version="1.0.0",
)

# In-memory database
books_db = {}
book_counter = 0


# PYDANTIC MODELS (Data Validation)
class Book(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Book name")
    author: str = Field(..., min_length=1, max_length=100, description="Author name")
    isbn: str = Field(
        ..., min_length=13, max_length=13, description="ISBN number (13 characters)"
    )
    published_year: int = Field(
        ..., ge=1000, le=2100, description="Year the book was published"
    )
    pages: int = Field(..., gt=0, description="Total number of pages")
    available: bool = Field(default=True, description="Availability status")
    genre: str = Field(..., description="Genre of the book")
    summary: str | None = Field(
        default=None, max_length=1000, description="Optional summary of the book"
    )

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
                "summary": "A classic American novel set in the 1920s",
            }
        }


class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    author: str | None = Field(None, min_length=1, max_length=100)
    isbn: str | None = Field(
        None,
        min_length=13,
        max_length=13,
    )
    published_year: int | None = Field(None, ge=1000, le=2100)
    pages: int | None = Field(None, gt=0)
    available: bool | None = None
    genre: str | None = None
    summary: str | None = Field(None, max_length=1000)


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    published_year: int
    pages: int
    available: bool
    genre: str
    summary: str
    added_at: str


class LibraryStats(BaseModel):
    total_books: int
    available_books: int
    borrowed_books: int
    total_pages: int
    average_pages: float
    books_per_genre: dict[str, int]
    books_per_author: dict[str, int]


# API ENDPOINT
# ROOT ENDPOINT
@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to Product Management API",
        "docs": "/docs",
        "total_products": len(books_db),
    }


# GET ALL BOOKS (with query parameters for filtering)
@app.get("/books", response_model=List[BookResponse], tags=["Books"])
def get_all_books(
    genre: str | None = Query(None, description="Filter by genre"),
    author: str | None = Query(None, description="Filter by author"),
    available: bool | None = Query(None, description="Filter by book availability"),
    min_pages: int | None = Query(None, ge=0, description="Filter by description"),
    max_pages: int | None = Query(None, ge=0, description="Filter by max_pages"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
):
    filtered_books = list(books_db.values())

    # Apply filter
    if genre:
        filtered_books = [
            b for b in filtered_books if b["genre"].lower() == genre.lower()
        ]

    if min_pages is not None:
        filtered_books = [b for b in filtered_books if b["pages"] >= min_pages]

    if max_pages is not None:
        filtered_books = [b for b in filtered_books if b["pages"] <= max_pages]

    if author:
        filtered_books = [
            b for b in filtered_books if b["author"].lower() == author.lower()
        ]

    if available is not None:
        filtered_books = [b for b in filtered_books if b["available"] == available]

    # Pagination
    paginated_books = filtered_books[skip : skip + limit]

    return paginated_books


# GET SINGLE BOOK
@app.get("/books/{book_id}", response_model=BookResponse, tags=["Books"])
def get_book(
    book_id: int = Path(
        ..., gt=0, description="This is the ID to get a particular book"
    )
):
    if book_id not in books_db:
        raise HTTPException(
            status_code=404, detail=f"Book is not found with this {book_id}"
        )

    return books_db[book_id]


# CREATE BOOKS (POST with request body)
@app.post("/books", response_model=BookResponse, status_code=201, tags=["Books"])
def create_books(book: Book):
    global book_counter
    book_counter += 1

    book_data = {
        "id": book_counter,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "published_year": book.published_year,
        "pages": book.pages,
        "available": book.available,
        "genre": book.genre,
        "summary": book.summary,
        "added_at": datetime.now().isoformat(),
    }

    books_db[book_counter] = book_data

    return book_data


# UPDATE BOOK
@app.put("/books/{book_id}", response_model=BookResponse, tags=["Books"])
def update_book(
    book_id: int = Path(..., gt=0, description="This ID of book is updated."),
    book_update: BookUpdate = None,
):
    if book_id not in books_db:
        raise HTTPException(
            status_code=404, detail=f"Book is not found with this {book_id}"
        )

    previous_book = books_db[book_id]

    # Update only provided fields
    update_data = book_update.model_dump(exclude_unset=True)

    for filed, value in update_data.items():
        previous_book[filed] = value

    books_db[book_id] = previous_book

    return previous_book


# DELETE BOOK
@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(
    book_id: int = Path(..., gt=0, description="This ID of book is deleted.")
):
    if book_id not in books_db:
        raise HTTPException(
            status_code=404, detail=f"Book is not found with this {book_id}"
        )

    deleted_book = books_db.pop(book_id)

    return {
        "message": "Book deleted successfully",
        "deleted_books": deleted_book,
    }


# SEARCH PRODUCTS
@app.get("/search/{author}/books", response_model=List[BookResponse], tags=["Search"])
def search_by_author(
    author: str = Path(..., description="Filter by author"),
    available: bool | None = Query(None, description="Pass query as an available"),
    genre: str | None = Query(None, description="Pass query as a genre"),
):
    filtered_books = list(books_db.values())

    if genre:
        filtered_books = [
            b for b in filtered_books if b["genre"].lower() == genre.lower()
        ]

    if author:
        filtered_books = [
            b for b in filtered_books if b["author"].lower() == author.lower()
        ]

    if available is not None:
        filtered_books = [b for b in filtered_books if b["available"] == available]

    return filtered_books


# STATISTICS ENDPOINT
@app.get("/stats", response_model=LibraryStats, tags=["Stats"])
def get_library_stats():

    # Handle empty database
    if not books_db:
        return {
            "total_books": 0,
            "available_books": 0,
            "borrowed_books": 0,
            "total_pages": 0,
            "average_pages": 0.0,
            "books_per_genre": {},
            "books_per_author": {},
        }

    total_books = len(books_db)
    available_books = 0
    borrowed_books = 0
    total_pages = 0
    books_per_genre = {}
    books_per_author = {}

    for book in books_db.values():
        # Available vs Borrowed
        if book["available"]:
            available_books += 1
        else:
            borrowed_books += 1

        total_pages += book["pages"]

        genre = book["genre"]
        books_per_genre[genre] = books_per_genre.get(genre, 0) + 1

        author = book["author"]
        books_per_author[author] = books_per_author.get(author, 0) + 1

    average_pages = round(total_pages / total_books, 2)

    return {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books,
        "total_pages": total_pages,
        "average_pages": average_pages,
        "books_per_genre": books_per_genre,
        "books_per_author": books_per_author,
    }
