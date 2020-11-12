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


