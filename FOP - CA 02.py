#PREREQUISITE 1: Install 'tabulate' module (>>>pip install tabulate)
#PREREQUISITE 2: Download and save the attached pickle file (book1.pk1)

#importing necessary modules
import pickle
import os
import datetime
from tabulate import tabulate
from datetime import timedelta
import time

#Defining classes to store elements with common attributes and define functions for them
class Book:
    def __init__(self, title, author, isbn, status): 
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

class Library:
    def __init__(self):
        self.books = []
        self.load_books()   #Loading previously stored data
        
    def add_book(self, book):
         self.books.append(book)    #Adding the new book to the stored list
         book.status = "available"  #Mentioning default book status
         self.save_books()  #Saving modified list
         print()
         print(f"TITLE : {book.title}, AUTHOR : {book.author}, ISBN : {book.isbn}")
         print("**Book was added successfully!**")

    def borrow_book(self, isbn, borrowed_time = datetime.datetime.now().replace(microsecond=0), due_date = None):    #Taking current time (without microsecond) as borrowed_time 
        for book in self.books:
            if book.isbn == isbn and book.status == "available":    #Checking whether the book is available
                print()
                print(f"TITLE: {book.title} , AUTHOR: {book.author}, ISBN: {book.isbn}, STATUS: {book.status}")
                print("Do you want to borrow this book?")   #Displaying book's details and confirming whether it is the correct one
                while True:
                    choice = input("Yes(Y) or No(N) : ")
                    if choice == "Y":
                        book.status = "borrowed"
                        book.borrowed_time = borrowed_time #Defining borrowed_time
                        book.due_date = due_date    
                        book.due_date = book.borrowed_time.date() + timedelta(days=14)  #Calculating due_date by adding 14 days to the borrowed_date
                        self.save_books()
                        print(f"**Book was borrowed successfully!**")
                        print("Due Date :",book.due_date)
                        return  #Returning to main menu
                    elif choice == "N":
                            return  #Breaking the loop and returning to the main menu
                    else:
                        print("**INVALID OPTION!**")    #Returning back to the 'choice'
                return  #Breaking the while loop
        else :
            print("**Book is not found or is currently borrowed.**")

    def return_book(self, isbn, returned_time = datetime.datetime.now().replace(microsecond=0)):
        for book in self.books:
            if book.isbn == isbn and book.status == "borrowed":
                book.status = "available"
                book.returned_time = returned_time
                self.save_books()
                print("**Book was returned successfully!**")
                print(f"TITLE: {book.title} , AUTHOR: {book.author}, ISBN: {book.isbn}, STATUS: {book.status}, RETURNED TIME: {book.returned_time}")
                print()
                over_due = (book.returned_time.date() - book.due_date).days     #Checking whether the return is overdued
                if over_due>0:
                    print(f"Overdue By: (over_due) days")
                    print("Fined Amount: Rs.",over_due*10)  #If overdued, calulate the fine (Rs.10 for each day)
                else:
                    print(f"Overdue By: 0 days")
                return 
        else :
            print("**Book is not found or not borrowed.**")

    def view_available_books(self):
        print()
        print("Available Books:")
        available_books = ((book.title, book.author, book.isbn) for book in self.books if book.status == "available")
        if available_books :
            headers = ("Title", "Author", "ISBN")   #Mentioning attibutes of the table
            nested_table = tabulate(available_books, headers, tablefmt = "grid")    #Creating the table in grid format
            print(nested_table)

    def view_borrowed_books(self):
        print()
        borrowed_books = ((book.title, book.author, book.isbn, book.borrowed_time) for book in self.books if book.status == "borrowed")
        if borrowed_books :
            headers = ("Title", "Author", "ISBN", "Borrowed Date & Time")
            nested_table = tabulate(borrowed_books, headers, tablefmt = "grid")
            print(nested_table)
        
    def save_books(self):                       #Saving data in a file using 'pickle' module
        with open('books.pk1', 'wb') as f:  
            pickle.dump(self.books, f)

    def load_books(self):                       #Reloading data from the stored file
        if os.path.exists('books.pk1'):     
            with open('books.pk1', 'rb') as f:
                self.books = pickle.load(f)

library = Library() #Calling instance

#Creating user interface
def LMS():
    while True:
        print()
        print("="*31)
        print("LIBRARY MANAGEMENT SYSTEM (LMS)")
        print()
        print("1 - Add new book")
        print("2 - Borrow book")
        print("3 - Return book")                 #Giving options to select for a user friendly interface
        print("4 - View available books")
        print("5 - View borrowed books")
        print("Q - Quit")
        print()
        user_input = input("Enter your preference : ")
            
        if user_input == "1":
            while True:
                title = input("Enter book title (or 'M' to return to Main Menu): ")
                if title == 'M':
                    break     #Back to the loop
                author = input("Enter author's name (or 'M' to return to Main Menu): ")
                if author == 'M':
                    break
                isbn = input("Enter ISBN (or 'M' to return to Main Menu): ")
                if isbn == 'M':
                    break
                book = Book(title, author, isbn, status ="available")
                library.add_book(book)
                break

        elif user_input == "2":
            while True:            
                isbn = input("Enter book ISBN (or 'M' to return to Main Menu): ")
                if isbn == 'M':
                    break
                library.borrow_book(isbn)
                break       #Back to to main loop. If not mentioned 'break' here program will execute continously even after a condition is met.
            
        elif user_input == "3":
            while True:            
                isbn = input("Enter book ISBN (or 'M' to return to Main Menu): ")
                if isbn == 'M':
                    break
                library.return_book(isbn)
                break

        elif user_input == "4":
            library.view_available_books()

        elif user_input == "5":
            library.view_borrowed_books()

        elif user_input == "Q":
            print("**Exited the System.**")
            print("(If you want to get back to the LMS Main Menu, feel free to enter 'LMS()' at anytime)")
            print("Thank you!!!")
            return    #Exit the entire system
            
        else:
            print("**INVALID OPTION!**")    #Back to the main menu

LMS()
