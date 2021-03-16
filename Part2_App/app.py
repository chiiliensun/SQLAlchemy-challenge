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
measurement = Base.classes.measurement
stations = Base.classes.stations

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
        f"<a href='/api/v1.0/billingcountry'>billingcountry</a><br/>"
        f"<a href='/api/v1.0/countrytotal'>countrytotal</a><br/>"
        f"<a href='/api/v1.0/postcodes/USA'>postcodes/USA</a><br/>"
        f"<a href='/api/v1.0/countryitemtotals/USA'>countryitemtotals/USA</a><br/>"
        f"<a href='/api/v1.0/postcodeitemtotals/USA'>postcodeitemtotals/USA</a><br/>"
    )

@app.route("/api/v1.0/billingcountry")
def billingcountry():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all countries in billing history
    results = session.query(Invoices.BillingCountry).group_by(Invoices.BillingCountry).all()


    session.close()
