#import dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from datetime import date

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

##database setup
engine= create_engine('sqlite:///Resources/hawaii.sqlite')

# set automap base and define classes
Base= automap_base()
Base.prepare(engine, reflect= True)

# set up data tables
Measurement = Base.classes.measurement
Station= Base.classes.station

#Create session
session= Session(engine)

last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
date_year_ago= date.fromisoformat(last_date.date)-dt.timedelta(days=365)

#flask set up
import flask
from flask import Flask, jsonify

app= Flask(__name__)

@app.route("/")
def home():
    """List all available api routes."""
    return(f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&ltstart&gt,  eg: /api/v1.0/2016-4-20 <br/>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt,      eg:/api/v1.0/2016-4-20/2017-2-20   <br/>")


#########################################################################################
#################                              ##########################################
################ Route /api/v1.0/precipitation  #########################################
#################                              ##########################################
#########################################################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    """
    Return dates and precipitation observations from the last year
    """
    session= Session(engine)
    
# Perform a query to retrieve the data and precipitation scores
    prcp_query= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=date_year_ago).\
        order_by(Measurement.date.asc()).all()

    session.close()
    
    return jsonify({keys:values for keys, values in prcp_query})

#########################################################################################
#################                              ##########################################
################# Route /api/v1.0/stations     ##########################################
#################                              ##########################################
#########################################################################################

@app.route("/api/v1.0/stations")
def station():
    
    """
    Return stations
    """
    session= Session(engine)
    
# Perform a query to retrieve the station data  
    station_name=session.query(Station.id, Station.station).all()

    session.close()
    
    return jsonify({id:station for id, station in station_name})

#########################################################################################
#################                              ##########################################
################# Route /api/v1.0/tobs         ##########################################
#################                              ##########################################
#########################################################################################

@app.route("/api/v1.0/tobs")
def temperature():
    """
    Return dates and temperature observations from the last year
    """
    session= Session(engine)
    
# Perform a query to retrieve the temperature data
    temp_obs=session.query(Measurement.date, func.avg(Measurement.tobs)).group_by(Measurement.date).filter(Measurement.date>=date_year_ago).\
                order_by(Measurement.date.asc()).all()
    
    session.close()
    
    return jsonify({date:temp for date, temp in temp_obs})

#########################################################################################
#################                              ##########################################
################# Route /api/v1.0/<start>/<end> #########################################
#################                              ##########################################
#########################################################################################

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end=last_date.date):
    '''
    Return the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
    ''' 
    session= Session(engine)
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    
    end_date= dt.datetime.strptime(end, '%Y-%m-%d')
     
    [tmin,tavg, tmax]= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()[0]
    session.close()
    
    return jsonify([{"temp_min": tmin}, 
                    {"temp_avg": tavg}, 
                    {"temp_max": tmax}])      


if __name__ == "__main__":
    #i want to run my code
    app.run(debug=True, port=7000)

