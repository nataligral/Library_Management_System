### Library Management System

Library Management System written in Python, and SQLAlchemy

### Python
- Python is an interpreted, high-level, general-purpose programming language.
- Python can be used in database applications.

### SQLAlchemy
- SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the -   full power and flexibility of SQL.

- It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.


The Library Management System will have the following listed features:

1. Books Catalogue Management
2. Customers Catalogue Management
3. Loans Catalogue Management

1. Book Catalogue Management
- Add new Book: 
•	Id (PK)
•	Name
•	Author 
•	Year Published 
•	Type (1/2/3):
    1 – up to 10 days
    2 – up to 5 days
    3 – up to 2 days
- Delete new Book

2. Customers Catalogue Management
- Add new Customer:
•	Id (PK)
•	Name
•	City
•	Age
- Remove Customer(change status)

3. Loans Catalogue Management
- Add new Loan:
•	CustID -FK
•	BookID-FK
•	Loandate
•	Returndate
- Remove Loan(return book)

3. Search
- Search book by name
- Search customer by name
- Search loan by book's name
	 


