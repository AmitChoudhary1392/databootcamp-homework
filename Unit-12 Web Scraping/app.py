from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

#Create instance for Flask app
app= Flask(__name__)

#Create connection to Mongo database
app.config["MONGO_URI"]= "mongodb://localhost:27017/Mission_to_Mars"

mongo= PyMongo(app)

#create routes to render index.html
@app.route("/")
def index():
    mars_data= mongo.db.mars_data.find_one()
    return render_template("index.html", data= mars_data)

#create route to scrape new data
@app.route("/scrape")
def scrape():
    
    #call scrape function to scrape new data 
    mars_data=scrape_mars.scrape_all()
    
    #Add scraped data to the database
    mongo.db.mars_data.update({}, mars_data, upsert=True)
    
    return redirect("http://localhost:5000/", code=302)

if __name__== "__main__":
    app.run(debug=True)