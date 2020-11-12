# import dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

######################################################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database and tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


# ########set session engine
session = Session(engine)

# query the last date in the database
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Calculate a 12month query duratioon from the last data point in the database
query_date = dt.date(2017,8,23) - dt.timedelta(days=365)

session.close()
######################################################

##### CREATE AN APP  ######
app = Flask(__name__)

#Use Flask to create your routes
@app.route("/")
def home():
    """List all available api routes."""
    return(
        f" Welcome to Hawaii Climate Homepage <br/> "
        f"Available Routes:<br/>"
        f"<br/>"  
        f"The list of precipitation data and dates:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"List of stations and names:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"List of 12 months temperature observations from the last data point:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Min, Max. and Avg. temperatures for chosen start date: (please use 'yyyy-mm-dd' format):<br/>"
        f"/api/v1.0/min_max_avg/&lt;start date&gt;<br/>"
        f"<br/>"
        f"Min. Max. and Avg. temperatures using start and end dates: (please use 'yyyy-mm-dd'/'yyyy-mm-dd' format for start and end values):<br/>"
        f"/api/v1.0/min_max_avg/&lt;start date&gt;/&lt;end date&gt;<br/>"
        f"<br/>"
        f"i.e. <a href='/api/v1.0/min_max_avg/2016-08-23/2017-08-23' target='_blank'>/api/v1.0/min_max_avg/2016-08-23/2017-08-23</a>"
    )

###### END OF LIST OF ROUTES

##### CREATE DATA WITH PRECIPITATION ROUTE 
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session engine
    session = Session(engine)

    """Dipplay dictionary for date and precipitation data"""
    # Query precipitation data and date values 
    results = session.query(Measurement.date, Measurement.prcp).all()
        
    session.close()
    
    # Create a dictionary using date as the key and precipitation as the value.
    precipitation = []
    for result in results:
        r = {}
        r[result[0]] = result[1]
        precipitation.append(r)

    return jsonify(precipitation )
##### END OF DATA WITH PRECIPITATION ROUTE 



####### CREATE STATION DATASET  

@app.route("/api/v1.0/stations")
def stations():
    # Create the session engine
    session = Session(engine)
    
    """Return a JSON list of stations from the dataset."""
    # Query stations list data
    results = session.query(Station.station, Station.name).all()
    
    session.close()
#list of dicts for each station
    station_list = []
    for result in results:
        r = {}
        r["station"]= result[0]
        r["name"] = result[1]
        station_list.append(r)
    
    # jsonify list
    return jsonify(station_list)

    #### END OF STATION DATASET



    #### CREATE TEMPERATURE DATASET
@app.route("/api/v1.0/tobs")
def tobs():
    # create session engine
    session = Session(engine)