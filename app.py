import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

base = automap_base()
base.prepare(engine, reflect=True)
measurement = base.classes.measurement
station = base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"Routes available on this site:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(measurement.date, measurement.prcp).group_by(measurement.date).order_by(measurement.date.desc()).limit(365).all()
    precip = {date: prcp for date, prcp in last_date}
    return precip

@app.route("/api/v1.0/stations")
def stations():
    stat = session.query(station.station).all()
    station_list = list(np.ravel(stat))
    return station_list


@app.route("/api/v1.0/tobs")
def temps():
    sel = [measurement.date, measurement.tobs]
    last_date_selected = session.query(*sel).group_by(measurement.date).order_by(measurement.date.desc()).filter(measurement.station =='USC00519281').limit(356).all()
    temperature = {date: tobs for date, tobs in last_date_selected}
    return temperature



if __name__ == '__main__':
    app.run()