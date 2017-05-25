from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sys, os, time
import requests
import json
import pandas as pd

APP_NAME = 'Fraud Detection API'
APP_DESCRIPTION = 'Determine the likelyhood of fraud'

#database = fraudsters
#table = dataframe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/fraudsters'
db = SQLAlchemy(app)

# Set homepage to index.html
#@app.route('/', methods = ['GET','POST'])
@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/predict')

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    x = {'date':[u'2012-06-28', u'2012-06-29', u'2012-06-30'], 'users': [405, 368, 119]}




    # x = 1 #dataframe.query.first(risk_level)
    # y = 2 #dataframe.query.first(fraud_probability)
    return render_template('predict.html', x=x)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    app.config['DEBUG'] = True
