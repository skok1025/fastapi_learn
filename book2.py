from typing import Optional

import uvicorn
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = None  # 선택적인 항목
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    # Example Value 값을 아래 Config 에서 지정해줄 수 있습니다.
    class Config:
        json_schema_extra = {
            "example": {
                "title": "A new book",
                "author": "Kim",
                "description": "Description 1234",
                "rating": 3,
                "published_date": 2023
            }
        }


BOOKS = [
    Book(1, "Title One", "Author One", "Description One", 5, 2019),
    Book(2, "Title Two", "Author Two", "Description Two", 3, 2020),
    Book(3, "Title Three", "Author Three", "Description Three", 3, 2019),
    Book(4, "Title Four", "Author Four", "Description Four", 2, 2019),
    Book(5, "Title Five", "Author Five", "Description Five", 1, 2019),
    Book(6, "Title Six", "Author Six", "Description Six", 0, 2023),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0, le=len(BOOKS))):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/")
async def read_book_by_rating(book_rating: int):
    books_return = []

    for book in BOOKS:
        if book.rating == book_rating:
            books_return.append(book)

    return books_return


@app.get("/books-by-date/")
async def read_book_publish_date(publish_date: int):
    books_return = []

    for book in BOOKS:
        if book.published_date == publish_date:
            books_return.append(book)

    return books_return


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    # ** 은 dictionary 를 키워드 형태로 변환해줍니다.
    # book_request 유효성검사는 아래 코드가 실행전에 진행됩니다.
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book


@app.put("/books/update_book")
async def update_book(book_request: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_request.id:
            BOOKS[i] = book_request

            return BOOKS[i]


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0, le=len(BOOKS))):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
