from fastapi import FastAPI, Body
import uvicorn

app = FastAPI()


BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]


@app.get("/")
async def first_api():
    return {"message": "Hello World"}


@app.get("/books")
async def read_all_books():
    return BOOKS


# first find end-point
@app.get("/books/mybook")
async def read_my_book():
    return {"title": "My Book", "author": "Me", "category": "fiction"}


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    # path variable
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book

    return {"error": "Book not found"}


@app.get("/books/")
async def read_books_by_category(category: str):
    # query parameter
    books_return = []

    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_return.append(book)

    return books_return


@app.post("/books/create-book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update-book")
async def update_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == update_book.get("title").casefold():
            BOOKS[i] = update_book
            return {"message": "Book updated successfully"}


@app.delete("/books/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}


@app.get("/books/byauthor/{author_name}")
async def read_books_by_author(author_name: str):
    books_return = []

    for book in BOOKS:
        if book.get("author").casefold() == author_name.casefold():
            books_return.append(book)

    return books_return


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)