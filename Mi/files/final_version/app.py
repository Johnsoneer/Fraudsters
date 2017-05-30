from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sys, os, time
import requests
import json
import pandas as pd
from sqlalchemy import create_engine, MetaData
import psycopg2
import numpy as np

APP_NAME = 'Fraud Detection API'
APP_DESCRIPTION = 'Determine the likelyhood of fraud'

#database = fraudsters
#table = dataframe

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://10.8.81.53/fraudsters'
# db = SQLAlchemy(app)

# engine = create_engine('postgresql://10.8.81.53/fraudsters', convert_unicode=True)
# x = MetaData()
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))

# conn = psycopg2.connect('postgresql://William:tiger@10.8.81.53:5432/fraudsters')
# cur = conn.cursor()
# cur.execute("SELECT org_name,risk_level,fraud_probability FROM dataframe;")
# query = cur.fetchone()
# df = pd.DataFrame(list(query)).T

conn = psycopg2.connect('postgresql://William:tiger@10.8.81.53:5432/fraudsters')
cur = conn.cursor()
cur.execute("SELECT org_name, risk_level, fraud_probability FROM dataframe WHERE risk_level = 'high' GROUP BY org_name,risk_level,fraud_probability;")
query = cur.fetchall()
df = pd.DataFrame(list(query)).T
df.iloc[2] = np.around(list(df.iloc[2]), 2)
# df.round({'Fraud Probability' : 2})

# cast(round(630/60.0,2) as numeric(36,2))

# print df.shape

# Set homepage to index.html
#@app.route('/', methods = ['GET','POST'])
@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/predict')

@app.route('/predict', methods = ['GET', 'POST'])
def predict():

    x = df
    y = df.shape[1]
    return render_template('predict.html', x=x, y=y)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    app.config['DEBUG'] = True
