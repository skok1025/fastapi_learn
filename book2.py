from fastapi import FastAPI
from pydantic import BaseModel, Field

import uvicorn

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: int
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)


BOOKS = [
    Book(1, "Title One", "Author One", "Description One", 5),
    Book(2, "Title Two", "Author Two", "Description Two", 4),
    Book(3, "Title Three", "Author Three", "Description Three", 3),
    Book(4, "Title Four", "Author Four", "Description Four", 2),
    Book(5, "Title Five", "Author Five", "Description Five", 1),
    Book(6, "Title Six", "Author Six", "Description Six", 0),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    # ** 은 dictionary 를 키워드 형태로 변환해줍니다.
    # book_request 유효성검사는 아래 코드가 실행전에 진행됩니다.
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
