import sqlite3
from Business import Book

DB_FILE = "Final.sqlite"

# Global variable for the database connection
conn = None

def connect():
    global conn
    if not conn:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
    return conn

def close():
    global conn
    if conn:
        conn.close()
        conn = None

def create_table():
    conn = connect()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS Book (
                        Book_ID INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        checked_out INTEGER DEFAULT 0,
                        due_date TEXT,
                        status TEXT DEFAULT 'Available'
                     )''')

def add_book(book):
    conn = connect()
    with conn:
        conn.execute('''INSERT INTO Book (Book_ID, title, author, checked_out, due_date, status) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (book.book_id, book.title, book.author, book.checked_out, book.due_date, book.status))

def get_books():
    conn = connect()
    with conn:
        results = conn.execute('''SELECT Book_ID, title, author, checked_out, due_date, status FROM Book''').fetchall()

    books = []
    for row in results:
        book = Book(row["Book_ID"], row["title"], row["author"], row["checked_out"], row["due_date"], row["status"])
        books.append(book)
    return books

def find_book_by_id(book_id):
    conn = connect()
    with conn:
        result = conn.execute('''SELECT * FROM Book WHERE Book_ID = ?''', (book_id,)).fetchone()

    if result:
        return Book(result["Book_ID"], result["title"], result["author"], result["checked_out"], result["due_date"], result["status"])
    else:
        return None
    
def update_book(book):
    conn = connect()
    with conn:
        conn.execute('''UPDATE Book SET title=?, author=?, checked_out=?, due_date=?, status=? WHERE Book_ID=?''',
                     (book.title, book.author, book.checked_out, book.due_date, book.status, book.book_id))

if __name__ == "__main__":
    create_table()
