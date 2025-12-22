# Library Management API

A modern, feature-rich REST API for managing library books built with **FastAPI** and **Pydantic**.

## 📋 Features

- ✅ Full CRUD operations for books
- ✅ Advanced filtering and searching capabilities
- ✅ Comprehensive data validation with Pydantic models
- ✅ Query parameters for pagination and filtering
- ✅ Library statistics endpoint
- ✅ Automatic API documentation (Swagger UI & ReDoc)
- ✅ In-memory database for quick prototyping

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone or navigate to the project directory:**

```bash
cd learn-fastapi
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the server:**

```bash
uvicorn module3-solution:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Base URL

```
http://localhost:8000
```

## 🔌 API Endpoints

### Root Endpoint

- **GET** `/` - Welcome message with API info

### Books Management

#### Get All Books

```http
GET /books
```

**Query Parameters:**

- `genre` (string) - Filter by book genre
- `author` (string) - Filter by author name
- `available` (boolean) - Filter by availability status
- `min_pages` (integer) - Minimum number of pages
- `max_pages` (integer) - Maximum number of pages
- `skip` (integer, default: 0) - Number of items to skip
- `limit` (integer, default: 10, max: 100) - Number of items to return

**Example:**

```bash
curl "http://localhost:8000/books?genre=Fiction&available=true&limit=5"
```

---

#### Get Single Book

```http
GET /books/{book_id}
```

**Path Parameters:**

- `book_id` (integer) - The ID of the book

**Example:**

```bash
curl "http://localhost:8000/books/1"
```

---

#### Create Book

```http
POST /books
```

**Request Body:**

```json
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "9780743273565",
  "published_year": 1925,
  "pages": 180,
  "available": true,
  "genre": "Fiction",
  "summary": "A classic American novel set in the 1920s"
}
```

**Status Code:** 201 Created

---

#### Update Book

```http
PUT /books/{book_id}
```

**Path Parameters:**

- `book_id` (integer) - The ID of the book

**Request Body (all fields optional):**

```json
{
  "title": "Updated Title",
  "author": "New Author",
  "available": false
}
```

---

#### Delete Book

```http
DELETE /books/{book_id}
```

**Path Parameters:**

- `book_id` (integer) - The ID of the book

---

### Search Endpoint

#### Search Books by Author

```http
GET /search/{author}/books
```

**Path Parameters:**

- `author` (string) - Author name to search

**Query Parameters:**

- `available` (boolean, optional) - Filter by availability
- `genre` (string, optional) - Filter by genre

**Example:**

```bash
curl "http://localhost:8000/search/Fitzgerald/books?genre=Fiction&available=true"
```

---

### Statistics Endpoint

#### Get Library Statistics

```http
GET /stats
```

**Response:**

```json
{
  "total_books": 5,
  "available_books": 3,
  "borrowed_books": 2,
  "total_pages": 850,
  "average_pages": 170.0,
  "books_per_genre": {
    "Fiction": 3,
    "Science": 2
  },
  "books_per_author": {
    "F. Scott Fitzgerald": 1,
    "Jane Austen": 1
  }
}
```

## 📊 Data Models

### Book (Request Model)

```python
{
  "title": str (1-200 chars, required),
  "author": str (1-100 chars, required),
  "isbn": str (13 chars, required),
  "published_year": int (1000-2100, required),
  "pages": int (>0, required),
  "available": bool (default: true),
  "genre": str (required),
  "summary": str (optional, max 1000 chars)
}
```

### BookResponse (Response Model)

Includes all fields from Book plus:

- `id`: Book ID (auto-generated)
- `added_at`: ISO format timestamp

## 🧪 Testing with Postman

Import the Postman collection using this link:

```
https://bholasankarnanda867-8376545.postman.co/workspace/Bholasankar-Nanda's-Workspace~c315fbc4-7143-45bd-85a0-c07bfa65735e/collection/49889071-53bd6383-6668-44c1-b935-bd4bf15442bb?action=share&source=copy-link&creator=49889071
```

This collection contains pre-configured requests for all API endpoints.

## 💾 Database

Currently uses an **in-memory database** (`books_db` dictionary). This data is lost when the server restarts. For production, consider integrating:

- SQLAlchemy ORM
- PostgreSQL/MySQL
- MongoDB

## 🛠️ Project Structure

```
learn-fastapi/
├── module3-solution.py      # Main FastAPI application
├── requirements.txt         # Project dependencies
├── README.md               # This file
├── docs/                   # Documentation folder
│   ├── module3-exercise.md
│   └── part2-products.md
└── __pycache__/            # Python cache
```

## 📦 Dependencies

See `requirements.txt` for all dependencies. Key packages:

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation

## 🔐 Validation Rules

- **Title:** 1-200 characters
- **Author:** 1-100 characters
- **ISBN:** Exactly 13 characters
- **Published Year:** Between 1000-2100
- **Pages:** Must be greater than 0
- **Summary:** Max 1000 characters (optional)

## 🐛 Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `201` - Created
- `404` - Book not found
- `400` - Bad request (validation error)
- `422` - Unprocessable entity

## 🚦 Example Usage

### Create a Book

```bash
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "1984",
    "author": "George Orwell",
    "isbn": "9780451526342",
    "published_year": 1949,
    "pages": 328,
    "available": true,
    "genre": "Dystopian"
  }'
```

### Get All Available Fiction Books

```bash
curl "http://localhost:8000/books?genre=Fiction&available=true"
```

### Update a Book

```bash
curl -X PUT "http://localhost:8000/books/1" \
  -H "Content-Type: application/json" \
  -d '{
    "available": false
  }'
```

### Delete a Book

```bash
curl -X DELETE "http://localhost:8000/books/1"
```

## 📝 Notes

- All timestamps are in ISO 8601 format
- Book IDs are auto-incremented starting from 1
- Case-insensitive filtering for genre and author
- Pagination uses skip/limit pattern (not page numbers)

## 🤝 Contributing

Feel free to modify and extend this API based on your needs!

## 📄 License

This project is open-source and available under the MIT License.

---

**Happy coding! 🎉**
