class Book:
    def __init__(self, book_id, title, author, checked_out=False, due_date=None, status="Available"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.checked_out = checked_out
        self.due_date = due_date
        self.status = status

    def __str__(self):
        return f"Book ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Status: {self.status}, Due Date: {self.due_date}"
