import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement= Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()
    
    all_dates = []
    for date, prcp in results:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["percipitation"] = prcp
        all_dates.append(rain_dict)

    return jsonify(all_dates)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def temps():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
#     query_date = dt.date(2016,8,23)
    
    results=session.query(Measurement.tobs).\
    filter(Measurement.station=='USC00519281').\
    filter(Measurement.date >= dt.date(2016,8,23)).all()

    session.close()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(results))

    return jsonify(all_temps)


@app.route("/api/v1.0/<start>")
def start_end_temps(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    start= dt.datetime.strptime(start, '%Y-%m-%d')

    temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    temps = list(np.ravel(temp))
    return jsonify(temps)



@app.route("/api/v1.0/<start>/<end>")
def start_temps(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    start= dt.datetime.strptime(start, '%Y-%m-%d')
    end = dt.datetime.strptime(end, '%Y-%m-%d')
    temp = session.query(func.min(Measurement.tobs), 
                         func.avg(Measurement.tobs), 
                         func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(temp))
    return jsonify(temps)



if __name__ == '__main__':
    app.run(debug=True)
