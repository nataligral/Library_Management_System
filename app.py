import json
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timedelta
from datetime import date

app = Flask(__name__)
CORS(app)
# Create SQLITE Database - myDb
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Library.sqlite3'
app.config['SECRET_KEY'] = "random string" 

db = SQLAlchemy(app)

 #// dictionary ot book dayb by type
books_days_by_type={1:10,2:5,3:2}

class Books(db.Model):
    id = db.Column('Book_id',db.Integer, primary_key = True)
    Name_B = db.Column(db.String(30))
    Author= db.Column(db.String(30))
    Year_published_B = db.Column(db.Integer)
    Type_Book_B = db.Column(db.Integer)
    books = db.relationship('Loans', backref='books')
    def __init__(self,Name_B,Author,Year_published_B,Type_Book_B):
        self.Name_B = Name_B
        self.Author = Author
        self.Year_published_B = Year_published_B
        self.Type_Book_B = Type_Book_B


class Customers(db.Model):
    id = db.Column('Customer_id',db.Integer, primary_key = True)
    Name_C = db.Column(db.String(50))
    City_C = db.Column(db.String(50))
    Age_C = db.Column(db.Integer)
    customer_status = db.Column(db.String(10))
    customers = db.relationship('Loans', backref='customers')
    def __init__(self, Name_C, City_C, Age_C,customer_status):
        self.Name_C = Name_C
        self.City_C = City_C
        self.Age_C = Age_C
        self.customer_status = customer_status


class Loans(db.Model):
    id = db.Column('Loan_id',db.Integer, primary_key = True)
    Loandate_L = db.Column(db.String(50))
    Returndate_L = db.Column(db.String(50))
    Customer_id = db.Column(db.Integer, db.ForeignKey('customers.Customer_id'))
    Book_id =db.Column(db.Integer, db.ForeignKey('books.Book_id'))
    # loan_status = db.Column(db.String(50))
    def __init__(self, Loandate_L,Returndate_L,Customer_id=0,Book_id=0):
        self.Loandate_L = Loandate_L
        self.Returndate_L = Returndate_L
        # self.loan_status=loan_status
        self.Customer_id=Customer_id
        self.Book_id=Book_id
        
# model Books
#Book Views
@app.route('/Books/<id>',methods = ['GET','DELETE'])
@app.route('/Books/', methods = ['GET', 'POST'])
def crude_Books(id=-1):
    if request.method=="POST":
        request_data = request.get_json()
        Name_B= request_data['Name_B']
        Author= request_data['Author']
        Year_published_B= request_data['Year_published_B']
        Type_Book_B= int(request_data['Type_Book_B'])
        if(not(Type_Book_B>=1)and(Type_Book_B<=3)):  #  //Check if the value is between 1 and 3//
            return "Book type must to be between 1 - 3 ", 400 
        newBook= Books(Name_B,Author,Year_published_B,Type_Book_B)
        db.session.add (newBook)
        db.session.commit()
        return "a new book was added"

    if request.method=="GET":
        res=[]
        for book in Books.query.all():
            res.append({"Book_id":book.id,"Name_B":book.Name_B,"Author":book.Author,"Year_published_B":book.Year_published_B,"Type_Book_B":book.Type_Book_B})
        return  (json.dumps(res)) 
        
    if request.method == 'DELETE':
        del_Book= Books.query.get(id)
        db.session.delete(del_Book)
        db.session.commit()
        return  'A Book Was Deleted'

# model Customers
#Customers Views
@app.route('/Customers/<id>',methods = ['GET','DELETE','PUT'])
@app.route('/Customers/', methods = ['GET', 'POST'])
def crude_Customers(id=-1):
    if request.method=="POST":
        request_data = request.get_json()
        Name_C= request_data["Name_C"]
        City_C= request_data["City_C"]
        Age_C= request_data["Age_C"]
        customer_status = request_data["customer_status"]
        newCustomer= Customers(Name_C,City_C,Age_C,customer_status)
        db.session.add (newCustomer)
        db.session.commit()
        return "a new Customer was added"

    if request.method=="GET":
        res=[]
        for Customer in  Customers.query.all():
            res.append({"Customer_id":Customer.id,"Name_C":Customer.Name_C,"City_C":Customer.City_C,"Age_C":Customer.Age_C,"customer_status":Customer.customer_status})
        return  (json.dumps(res))

    if request.method == 'DELETE':
        del_Customer= Customers.query.get(id)
        db.session.delete(del_Customer)
        db.session.commit()
        return  'A Customer Was Deleted'

    if request.method == 'PUT':
            request_data = request.get_json()
            upd_customer = Customers.query.get(id)
            if upd_customer:
                upd_customer.customer_status =request_data["customer_status"]
                db.session.commit()
            return "A customer was update "


# model Loans
#Loans Views
@app.route('/Loans/<id>',methods = ['PUT','DELETE'])
@app.route('/Loans/', methods = ['GET', 'POST'])
def crude_Loans(id=-1):
    if request.method=="POST":
        request_data = request.get_json()
        Loandate_L = request_data['Loandate_L']
        Customer_id= request_data['Customer_id']
        Book_id= request_data['Book_id']
        book=Books.query.get(Book_id) #// get all the Parameters of the book
        Returndate_L= datetime.strptime(Loandate_L, "%Y-%m-%d")+ timedelta(days=books_days_by_type[book.Type_Book_B]) #//make a conversion and calculate the return date of the book according to the value of the key in the dictionary
        newLoan= Loans(Loandate_L,Returndate_L.date(),Customer_id,Book_id)
        db.session.add (newLoan)
        db.session.commit()
        return ("a new Loan was added")

    if request.method == 'GET': 
        res=[]
        for Loan,Book,Customer in db.session.query(Loans,Books,Customers).join(Books).join(Customers):
            load_date = datetime.strptime(Loan.Returndate_L, "%Y-%m-%d")
            print(Loan.Returndate_L)
            now =  datetime.now() # today date
            loan_status = ""
            if (now.date() < load_date.date()): # If the return date is later than today, the customer is on time
                loan_status = "on time" # Table status-"on time"
            elif (now.date() == load_date.date()): # If the return date is today, the customer needs to return the book at most today
                loan_status = "due date" # Table status-"due date"
            else:
                loan_status = "late" # If the return date has passed, the customer is late in returning the book. Table status-"late"
            res.append({"Loan_id":Loan.id,
                        "Customer_id":Loan.Customer_id,
                        "Book_id":Loan.Book_id,
                        "Loandate_L":Loan.Loandate_L,
                        "Returndate_L":Loan.Returndate_L,
                        "loan_status":loan_status,
                        "Type_Book_B":Book.Type_Book_B,
                        "Name_B":Book.Name_B,
                        "Name_C":Customer.Name_C,
                        "Customer_id":Customer.id})
        return (json.dumps(res))   

    if request.method == 'PUT':
            request_data = request.get_json()
            upd_loan = Loans.query.get(id)
            if upd_loan:
                upd_loan.Returndate_L =request_data["Returndate_L"]
                db.session.commit()
            return "A Loan was updated "
 
    if request.method == 'DELETE':
        del_loan= Loans.query.get(id)
        db.session.delete(del_loan)
        db.session.commit()
        return "A book was returned"

if __name__ == '__main__':
    with app.app_context():db.create_all()
    app.run(debug = True)