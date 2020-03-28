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
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://xuogxhiwjayrke:c8a1bc208e9b818bfa20e9e23ee06c5fe8857d6becc336912a42184706764b3b@ec2-184-72-236-3.compute-1.amazonaws.com:5432/d2ma2m4n786kvk"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:postgres@localhost:5432/BookShare"
db = SQLAlchemy(app)

class Library(db.Model):
    __tablename__ = 'Library'

    id_book = db.Column(db.String(20), primary_key=True) 
    title = db.Column(db.String(300))
    description = db.Column(db.String(5000))
    category=db.Column(db.String(30))
    sub_category= db.Column(db.String(50))
    isbn = db.Column(db.String(13))
    image_url = db.Column(db.String(1000))
    author = db.Column(db.String(500))
    published_date = db.Column(db.Date)
    publisher = db.Column(db.String(100))
    language = db.Column(db.String(2))
    num_pages=db.Column(db.Float)
    ratings_count=db.Column(db.Float)
    reviews_count=db.Column(db.Float)
    text_reviews_count=db.Column(db.Float)
    average_rating=db.Column(db.Float)

    def __repr__(self):
        return '<Library %r>' % (self.title)

class Book(db.Model):
    __tablename__ = 'Book'

    id_book = db.Column(db.String(20), primary_key=True) 
    title = db.Column(db.String(300))
    description = db.Column(db.String(5000))
    category=db.Column(db.String(30))   
    isbn = db.Column(db.String(13))
    image_url = db.Column(db.String(1000))
    author = db.Column(db.String(500))
    published_date = db.Column(db.Date)
    publisher = db.Column(db.String(100))
    language = db.Column(db.String(2))

    def __repr__(self):
        return '<Book %r>' % (self.title)
        

class Owner(db.Model):
    __tablename__ = 'Owner'

    id_book = db.Column(db.String(20), primary_key=True) 
    owner_email = db.Column(db.String(60), primary_key=True)
    rating = db.Column(db.Float)
    review = db.Column(db.String(1000))
    location = db.Column(db.String(150))
    lat= db.Column(db.Float(10))
    lon= db.Column(db.Float(10))
    contact_details = db.Column(db.String(1000))
    available = db.Column(db.Integer)

    def __repr__(self):
        return '<Owner %r>' % (self.owner_email)