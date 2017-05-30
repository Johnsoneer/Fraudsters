from flask import Flask, render_template, request
import sys, os, time
import requests
import json
import pandas as pd
from flask.ext.sqlalchemy import SQLAlchemy
import psycopg2

APP_NAME = 'Fraud Detection API'
APP_DESCRIPTION = 'Determine the likelyhood of fraud'

#database = fraudsters
#table = dataframe

conn = psycopg2.connect('postgresql://William:tiger@10.8.81.53:5432/fraudsters')
cur = conn.cursor()
cur.execute("SELECT org_name,risk_level,fraud_probability FROM dataframe;")
query = cur.fetchone()

print query

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://William:tiger@10.8.81.53:5432/fraudsters'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    x = User.query.filter_by(email=email).first()
    return render_template('predict.html', x=x)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    app.config['DEBUG'] = True
