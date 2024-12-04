import db
from Business import Book
from datetime import datetime, timedelta
from contextlib import closing

def add_book():
    title = input("Title: ")
    author = input("Author: ")
    book_id = input("Book ID: ")
    
    existing_book = db.find_book_by_id(book_id)
    if existing_book:
        # Update the existing entry
        existing_book.title = title
        existing_book.author = author
        db.update_book(existing_book)
        print("Book updated successfully!\n")
    else:
        # Add a new book
        conn = db.connect()  # Open the database connection
        with conn:
            db.add_book(Book(book_id, title, author))
        print("Book added successfully!\n")

def list_books():
    conn = db.connect()
    with closing(conn.cursor()) as c:
        c.execute('''SELECT Book_ID, title, author, checked_out, due_date, status 
                     FROM Book''')  
        results = c.fetchall()

    books = []
    for row in results:
        book = Book(row["Book_ID"], row["title"], row["author"], row["checked_out"], row["due_date"], row["status"])
        books.append(book)

    if not books:
        print("No books available.")
    else:
        for book in books:
            print(book)
    print()


def check_out_book(access_date):
    book_id = input("Enter the Book ID of the book to check out: ")
    book = db.find_book_by_id(book_id)
    if book:
        if book.checked_out:
            print("This book is already checked out.")
        else:
            # Nested if statement 
            user_confirmation = input("Do you want to proceed with checking out this book? (yes/no): ")
            if user_confirmation.lower() == "yes":
                book.checked_out = True
                due_date = access_date + timedelta(days=7)  # 7 days due period
                book.due_date = due_date.strftime("%Y-%m-%d")
                book.status = "Not Available"  # Update status to "Not Available" when checked out
                db.update_book(book)
                print(f"Successfully checked out. Due date: {due_date.strftime('%Y-%m-%d')}")
            else:
                print("Check out process canceled.")
            # End of nested if statement
    else:
        print("Book not found.")
        
def check_in_book():
    book_id = input("Enter the Book ID of the book to check in: ")
    book = db.find_book_by_id(book_id)
    if book:
        if not book.checked_out:
            print("This book is already available.")
        else:
            # Nested if statement begins here
            user_confirmation = input("Do you want to proceed with checking in this book? (yes/no): ")
            if user_confirmation.lower() == "yes":
                book.checked_out = False
                book.due_date = None
                book.status = "Available"
                db.update_book(book)
                print("Successfully checked in.")
            else:
                print("Check in process canceled.")
            # End of nested if statement
    else:
        print("Book not found.")

def show_overdue_books(access_date):
    books = db.get_books()
    overdue_books = [book for book in books if book.checked_out and datetime.strptime(book.due_date, "%Y-%m-%d") < access_date]
    
    if not overdue_books:
        print("No overdue books.")
    else:
        print("\nOverdue Books:")
        for book in overdue_books:
            print(book)


def main():
    print("Welcome to the Book Library System\n")
    db.connect()
    db.create_table()
    
    # Prompt user to input the date they are accessing the script
    access_date_str = input("Enter the date (YYYY-MM-DD) you are accessing the script: ")
    try:
        access_date = datetime.strptime(access_date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        return
    
    print("\nToday's Date:", access_date.strftime("%Y-%m-%d"))
    
    while True:
        print("\nMenu Options:")
        print("1. Add Book")
        print("2. List Books")
        print("3. Check Out Book")
        print("4. Check In Book")
        print("5. Show Overdue Books")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            add_book()
        elif choice == "2":
            list_books()
        elif choice == "3":
            check_out_book(access_date)
        elif choice == "4":
            check_in_book()
        elif choice == "5":
            show_overdue_books(access_date)
        elif choice == "6":
            print("Exiting program. Goodbye!")
            db.close()
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()

