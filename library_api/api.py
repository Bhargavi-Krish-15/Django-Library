# library_api/api.py
# library_api/api.py
import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from library.models import Book, Review
from django.contrib.auth.models import User

app = FastAPI(title="Library API", version="1.0.0")

# --- Pydantic Schemas ---
class BookSchema(BaseModel):
    id: int
    title: str
    author: list[str]
    description: str
    # average_rating: float

    class Config:
        from_attributes = True


class ReviewSchema(BaseModel):
    id: int
    user: str
    rating: int
    comment: str

    class Config:
        from_attributes = True


# --- API Endpoints ---
@app.get("/books/", response_model=list[BookSchema])
def list_books():
    books = Book.objects.all()
    return [
        BookSchema(
            id=b.id,
            title=b.title,
            author=[a.first_name for a in b.authors.all()],
            description=b.summary,
            # average_rating=b.average_rating(),
        )
        for b in books
    ]


@app.get("/books/{book_id}", response_model=BookSchema)
def get_book(book_id: int):
    try:
        book = Book.objects.get(id=book_id)
        return BookSchema(
            id=book.id,
            title=book.title,
            author=[a.first_name for a in book.authors.all()],
            description=book.summary,
            # average_rating=book.average_rating(),
        )
    except Book.DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/{book_id}/reviews", response_model=list[ReviewSchema])
def get_reviews(book_id: int):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise HTTPException(status_code=404, detail="Book Not Found")
    
    reviews = book.reviews.all()
    
    return [
        ReviewSchema(
            id=r.id,
            user=r.user.username,
            rating=r.rating,
            comment=r.comment
        ) for r in reviews
    ]

    
