from flask import Flask, jsonify
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
from time import strptime

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
date_threshold = dt.datetime(2016, 8, 23)

@app.route("/")
def home():
    print("This is the start.")
    return(
        "Welcome to the beginning.<br/>"
        f"Routes include:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/StartingYear<br/>"
        f"/api/v1.0/StartingYear/EndingYear<br/>"
        f"The last two routes require date inputs.")

@app.route("/api/v1.0/precipitation")
def precips():
    session = Session(engine)
    letsago = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > date_threshold).all()
    session.close()

    precips = []
    for date, prcp in letsago:
        precips_dict = {date: prcp}
        precips.append(precips_dict)

    return jsonify(precips)

@app.route("/api/v1.0/station")
def station():
    session = Session(engine)
    eurobeat_girls_ready_for_launch = session.query(Station.station).all()
    session.close()
    station_list = list(np.ravel(eurobeat_girls_ready_for_launch))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    engage = session.query(Measurement.tobs).filter(Measurement.date > date_threshold).filter(Measurement.station == 'USC00519281').all()
    session.close()
    tobs_list = list(np.ravel(engage))
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def gimmeadate(start):
    session = Session(engine)

    tobs_subquery = session.query(Measurement.date).filter(Measurement.date >= start)
    liftoff = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date.in_(tobs_subquery)).all()

    session.close()
    starts_list = list(np.ravel(liftoff))
    return jsonify(starts_list)

@app.route("/api/v1.0/<start>/<end>")
def gimmethedates(start, end):
    session = Session(engine)
    yallreadyforthis = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date.between(start, end)).all()
    session.close()
    start_end_list = list(np.ravel(yallreadyforthis))
    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)