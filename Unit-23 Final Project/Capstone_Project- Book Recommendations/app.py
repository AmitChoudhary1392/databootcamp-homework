# import necessary libraries
import os
import numpy as np
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

import requests

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

app.config['JSON_SORT_KEYS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://xuogxhiwjayrke:c8a1bc208e9b818bfa20e9e23ee06c5fe8857d6becc336912a42184706764b3b@ec2-184-72-236-3.compute-1.amazonaws.com:5432/d2ma2m4n786kvk"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:postgres@localhost:5432/BookShare"
db = SQLAlchemy(app)
db.create_all()

from models import *

# global variables used in the code
bookTitle=""
books=[]
books_owner=[]

# create route that renders index.html template
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

#navigation route
@app.route("/bookSearch", methods=["GET", "POST"])
def Find_Books():
    
    return render_template("Find_Books.html")

# Query the database and send the jsonified results
@app.route("/getBook", methods=["GET", "POST"])
def getBook():
    if request.method == "POST":
        
        bookTitle = request.form["title"]
        #print(bookTitle)
        
        ## sqlalchemy.ORM is not working so using sessions instead.
        connection_string = 'postgres:postgres@localhost:5432/BookShare'
        engine = create_engine(f'postgresql://{connection_string}')
        Base=automap_base()
        Base.prepare(engine, reflect=True)

        lib= Base.classes.library
        session=Session(engine)

        books_db = session.query(lib.id_book, lib.title, lib.image_url, lib.authors, lib.average_rating).\
                filter(lib.title.like(f'%{bookTitle}%')).limit(10).all()

        #print (books_db)
        global books
        books=[]
        for book in books_db:
            dict_book = {
                "id" : book[0],
                "title" : book[1],
                "image_url": book[2],
                "author":book[3],
                "average_rating":book[4]   
            }
            books.append(dict_book)
        
        session.close()
        """ data=jsonify(books)
        return data """      
    return render_template("Find_Books.html")

@app.route("/api/findbook")
def findbook():

    global books
    data= jsonify(books)
    books=[]
    return data

#################################################################################################################
# ###################         bookshare page and Owner Details    #################################################
###################################################################################################################

#navigation route
@app.route("/bookShare", methods=["GET", "POST"])
def Share_Books():
    
    return render_template("Share_Books.html")

@app.route("/getbooks_share", methods=["GET", "POST"])
def OwnerBooks():
    if request.method == "POST":
        bookTitle = request.form["title"]

        #Googlebooks API connection
        from config import google_api_key

        params={'key':google_api_key,
            'maxResults':5}

        url= f'https://www.googleapis.com/books/v1/volumes?q={bookTitle}'
        response = requests.get(url, params).json()

        global books_owner
        books_owner=[]
        
        #Extracting required information from Google books API
        results=response['items']
        for item in results:
            try:
                book={
                    'image_url':item['volumeInfo']['imageLinks']['smallThumbnail'] if 'imageLinks' in item['volumeInfo'].keys() else " ",
                    'id_book': item['id'],
                    'title':item['volumeInfo']['title'] if 'title' in item['volumeInfo'].keys() else " ",
                    'category/genre':item['volumeInfo']['categories'] if 'categories' in item['volumeInfo'].keys() else " ",
                    'authors':item['volumeInfo']['authors'] if 'authors' in item['volumeInfo'].keys() else " ",
                    'description': item['volumeInfo']['description'] if 'description' in item['volumeInfo'].keys() else " ",
                    'isbn':item['volumeInfo']['industryIdentifiers'][0]['identifier'] if 'industryIdentifiers' in item['volumeInfo'].keys() else " ",
                    'language':item['volumeInfo']['language'] if 'language' in item['volumeInfo'].keys() else " ",
                    'published_date':item['volumeInfo']['publishedDate'] if 'published_date' in item['volumeInfo'].keys() else " ",
                    'publisher': item['volumeInfo']['publisher'] if 'publisher' in item['volumeInfo'].keys() else " "     
                }
                
            except:
                book = {'id_book': 'not found'}
        
            books_owner.append(book)


    return render_template("Share_Books.html")

@app.route("/api/sharebook_results")
def sharebook_results():

    global books_owner
    dict_books=[]
    
    for book in books_owner:

            dict_book = {
                "image_url": book['image_url'],
                 "title" : book['title'],
                 "author":book['authors'],
                "id" : book['id_book']
                 }
            dict_books.append(dict_book)
    
    data= jsonify(dict_books)
    books_owner=[]

    return data

@app.route("/getuserinputs", methods=["GET", "POST"])
def OwnerDetails():
    
    return render_template("Owner_Details.html")


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    
    if request.method == "POST":
        title = request.form["title"]
        owner_email = request.form["email"]
        rating = request.form["rating"]
        review= request.form["review"]
        location= request.form["location"]
        contact_details= request.form["contact_details"]
        available= request.form["available"]

        from config import api_key
        params={'address':location,
                "key":api_key}

        url= 'https://maps.googleapis.com/maps/api/geocode/json?'
        response=requests.get(url, params).json()

        # getting lat/lng for the given address
        lat =response['results'][0]['geometry']['location']['lat']
        lon =response['results'][0]['geometry']['location']['lng']


###*** need to modify the owner table fields in database
    return redirect("/", code=302)


#################################################################################################################
# ###################         Books List and Books Stats    #################################################
###################################################################################################################
#navigation route

@app.route("/library", methods=["GET","POST"])
def Books_List():
    if request.method== "POST":
    
        connection_string = 'postgres:postgres@localhost:5432/BookShare'
        engine = create_engine(f'postgresql://{connection_string}')
        Base=automap_base()
        Base.prepare(engine, reflect=True)

        lib= Base.classes.library
        session=Session(engine)

        books_db = session.query(lib.image_url, lib.title, lib.authors, lib.average_rating).limit(20).all()

        #print (books_db)
        global books
        books=[]
        for book in books_db:
            dict_book = {
                "title" : book[1],
                "author":book[2],
                "average_rating":book[3],
                "image_url": book[0]   
            }
            books.append(dict_book)
        
        session.close()
    
    return render_template("Books_List.html")

@app.route("/api/bookList")
def Library():

    global books
    data= jsonify(books)
    books=[]
    return data
    
#navigation route
@app.route("/visualisations", methods=["GET", "POST"])
def visualisations():
    
    return render_template("Books_stats.html")


if __name__ == "__main__":
    app.run()