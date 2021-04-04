import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify
import datetime as dt


# Database Setup
    engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

    Base = automap_base()

    Base.prepare(engine, reflect=True)

    Measurement = Base.classes.measurement
    Station = Base.classes.station

    session = Session(engine)    
###------------------------------------------###



# Flask Setup and Routes

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
###------------------------------------------###


# Precipitation

import datetime as dt

def precipitation():
    
    latestdate = dt.date(2017, 8 ,23)
    oneyearago = maxDate - dt.timedelta(days=365)
    precquery = (session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <= latestdate)
                .filter(Measurement.date >= oneyearago).order_by(Measurement.date).all())

    return jsonify(precquery)
###------------------------------------------###


# Stations

@app.route('/api/v1.0/stations')
def stations():

    stationvar = session.query(Station.station).all()
    return jsonify(stationvar)
###------------------------------------------###


# Tobs

def tobs():  
    maxDate = dt.date(2017, 8 ,23)
    oneyearago = maxDate - dt.timedelta(days=365)

    latestyear = (session.query(Measurement.tobs)
                .filter(Measurement.station == 'USC00519281')
                .filter(Measurement.date <= maxDate)
                .filter(Measurement.date >= oneyearago)
                .order_by(Measurement.tobs).all())
    
    return jsonify(latestyear)
###------------------------------------------###


# Start

@app.route('/api/v1.0/<start>') 
def start(start=None):
    
    tobs = (session.query(Measurement.tobs).filter(Measurement.date.between(start, '2017-08-23')).all())
    
    tobsdf = pd.DataFrame(tobs)
    tavg = tobsdf["tobs"].mean()
    tmax = tobsdf["tobs"].max()
    tmin = tobsdf["tobs"].min()
    
    return jsonify(tmin, tmax, tavg)
###------------------------------------------###

# Start and End

@app.route('/api/v1.0/<start>/<end>') 
def startend(start=None, end=None):
    
    tobs = (session.query(Measurement.tobs).filter(Measurement.date.between(start, end)).all())
