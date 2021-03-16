# List all routes that are available.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# using class activities Stu-Chinook
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"<a href='/api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>Stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>Temperature Observations</a><br/>"
        f"<a href='/api/v1.0/<start>'>Start Temperature</a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>Date Range</a><br/>"
    )

# Precipitation Route - Results
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # create a dictionary from the row data and append to a list of all_results
    precip_all = []
    for item in results:
        item_dict = {}
        item_dict['date'] = item[0]
        item_dict['prcp'] = item[1]
        precip_all.append(item_dict)

    return jsonify(precip_all)

#####################################################
# Station Route - Results
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query results
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Return a JSON list of stations from the dataset
    # create a dictionary
    station_list = []
    for item in results:
        station_dict = {}
        station_dict['station'] = item[0]
        station_dict['name'] = item[1]
        station_list.append(station_dict)

    return jsonify(station_list)

#####################################################

# Temperature Observation Route - Results
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query similar to jupyter notebook, copy & paste!
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-24').order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the results
    tobs_list = []
    for item in results:
        tobs_dict = {}
        tobs_dict['station'] = item[0]
        tobs_dict['date'] = item[1]
        tobs_dict['tobs'] = item[2]
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

#####################################################

# Start Temperature Date Route - Results
@app.route("/api/v1.0/<start>")
def start_temp(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query and variable
    first_date = ('2016, 08, 23')
    results = session.query(Measurement.date, func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= first_date).group_by(Measurement.date).order_by(Measurement.date).all()

    session.close()

    # Return a JSON list of date, min, max, and avg from the dataset
    # create a dictionary
    start_temp_list = []
    for date, max, min, avg in results:
        start_temp_dict = {}
        start_temp_dict["date"] = date
        start_temp_dict["max"] = max
        start_temp_dict["min"] = min
        start_temp_dict["avg"] = avg
        start_temp_list.append(start_temp_dict)

    return jsonify(start_temp_list)


@app.route("/api/v1.0/<start>/<end>")
def range_temp(start, end):

# Create our session (link) from Python to the DB
    session = Session(engine)

    # query and variable
    start_date = ('2016, 08, 23')
    end_date = ('2017, 08, 23')
    results = session.query(Measurement.date, func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).group_by(Measurement.date).order_by(Measurement.date).all()

    session.close()

    # Return a JSON list of date, min, max, and avg from the dataset
    # create a dictionary
    range_list = []
    for date, max, min, avg in results:
        range_dict = {}
        range_dict["date"] = date
        range_dict["max"] = max
        range_dict["min"] = min
        range_dict["avg"] = avg
        range_list.append(range_dict)

    return jsonify(range_list)












if __name__ == '__main__':
    app.run(debug=True)
