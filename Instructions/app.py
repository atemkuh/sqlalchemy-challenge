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
        f"Welcome to Hawaii Climate Homepage <br/>"
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
        new_result = {}
        new_result[result[0]] = result[1]
        precipitation.append(new_result)

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
        new_result= {}
        new_result["station"]= result[0]
        new_result["name"] = result[1]
        station_list.append(new_result)
    
    # jsonify list
    return jsonify(station_list)

    #### END OF STATION DATASET



    #### CREATE TEMPERATURE DATASET
@app.route("/api/v1.0/tobs")
def tobs():
    # create session engine
    session = Session(engine)

    """ Return a json list of temperature observations(tobs) for the previous 12 months."""

    results = session.query(Measurement.tobs, Measurement.data).filter(Measurement.date >= query_date).all()
    session.closed()

    tobs_list = []
    for result in results:
        new_result = {}
        new_result["date"] = result[1]
        new_result["temprature"] = result[0]
        tobs_list.append(new_result)

    # jsonify the list
    return jsonify(tobs_list)

    @app.route("/api/v1.0/min_max_avg/<start>")
def start(start):
    # session engine
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""

    # query data using any date and convert to yyyy-mm-dd
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')

    # query session
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_dt).all()

    session.close()

    # Hold results using a list
    t_list = []
    for result in results:
        new_result = {}
        new_result["StartDate"] = start_dt
        new_result["TMIN"] = result[0]
        new_result["TAVG"] = result[1]
        new_result["TMAX"] = result[2]
        t_list.append(new_result)

    # jsonify the result
    return jsonify(t_list)

@app.route("/api/v1.0/min_max_avg/<start>/<end>")
def start_end(start, end):
    # create session engine
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start and end dates."""

    # Format query start & end dates and convert to yyyy-mm-dd
    start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
    end_dt = dt.datetime.strptime(end, "%Y-%m-%d")