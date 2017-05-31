# coding: utf-8
import pandas as pd
import datetime as dt
import cPickle as pickle
from sqlalchemy import create_engine
from time import sleep
import requests
import json
from flask import jsonify

def get_json():
    response = requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point')
    return json.loads(json.dumps(response.json()))

def model_load():
    return pickle.load(open('model.p', 'rb'))

def data_clean(readin, dummies):
    # point = pd.DataFrame([readin])
    point = pd.read_json(readin)
    orig = point.copy()
    datecols = ['approx_payout_date', 'event_created', 'event_end', 'event_start', 'event_published', 'user_created']

    convert = lambda x: dt.datetime.fromtimestamp(x)
    df_copy = point.copy()
    for i in datecols:
        df_copy[i]=df_copy[i].apply(pd.to_numeric)
        df_copy[i]=df_copy[i].apply(convert)

    df_copy['created_date'] = df_copy['event_created'].dt.date
    df_copy['started_date'] = df_copy['event_start'].dt.date
    # df['published_date'] = df['event_published'].dt.date
    df_copy['approx_payout_day'] = df_copy['approx_payout_date'].dt.date
    #Creating new column where TRUE if all dates are equal
    date_df = df_copy[['created_date','started_date']]
    date_df['all_equal'] = ((date_df['created_date']==date_df['started_date']))
    #(date_df[‘created_date’]==date_df[‘published_date’]) &
    # created_started = date_df[date_df['all_equal']==True]
    # sum(created_started['Fraud'])/float(len(created_started))
    point['all_equal'] = date_df['all_equal']

    keep_col = ['all_equal', 'body_length', 'channels', 'country', 'currency', \
                'delivery_method', 'event_created', 'event_end', 'event_published', 'event_start', \
                'fb_published', 'gts', 'has_analytics', 'has_logo', 'listed', \
                'name_length', 'num_order', 'num_payouts', 'org_facebook', 'org_twitter', \
                'payout_type', 'sale_duration', 'sale_duration2', 'show_map', 'user_age', \
                'user_created', 'user_type', 'venue_country', 'venue_latitude', 'venue_longitude', \
                'venue_state']
    point =  point[keep_col]
    for col in dummy_dict:
        values = dummy_dict[col]
        for value in values:
            point[(value + '_' + col)] = int(point[col] == value)
        point.pop(col)
    return (point, orig)

def data_cleanJ(readin, dummies):
    point = pd.DataFrame([readin])
    # point = pd.read_json(readin)
    orig = point.copy()
    datecols = ['approx_payout_date', 'event_created', 'event_end', 'event_start', 'event_published', 'user_created']

    convert = lambda x: dt.datetime.fromtimestamp(x)
    df_copy = point.copy()
    for i in datecols:
        df_copy[i]=df_copy[i].apply(pd.to_numeric)
        df_copy[i]=df_copy[i].apply(convert)

    df_copy['created_date'] = df_copy['event_created'].dt.date
    df_copy['started_date'] = df_copy['event_start'].dt.date
    # df['published_date'] = df['event_published'].dt.date
    df_copy['approx_payout_day'] = df_copy['approx_payout_date'].dt.date
    #Creating new column where TRUE if all dates are equal
    date_df = df_copy[['created_date','started_date']]
    date_df['all_equal'] = ((date_df['created_date']==date_df['started_date']))
    #(date_df[‘created_date’]==date_df[‘published_date’]) &
    # created_started = date_df[date_df['all_equal']==True]
    # sum(created_started['Fraud'])/float(len(created_started))
    point['all_equal'] = date_df['all_equal']

    keep_col = ['all_equal', 'body_length', 'channels', 'country', 'currency', \
                'delivery_method', 'event_created', 'event_end', 'event_published', 'event_start', \
                'fb_published', 'gts', 'has_analytics', 'has_logo', 'listed', \
                'name_length', 'num_order', 'num_payouts', 'org_facebook', 'org_twitter', \
                'payout_type', 'sale_duration', 'sale_duration2', 'show_map', 'user_age', \
                'user_created', 'user_type', 'venue_country', 'venue_latitude', 'venue_longitude', \
                'venue_state']
    point =  point[keep_col]
    for col in dummy_dict:
        values = dummy_dict[col]
        for value in values:
            point[(col + '_' + value)] = int(point[col] == value)
        point.pop(col)
    return (point, orig)

def pred_send(points, model):
    point, orig = points
    p = model.predict_proba(point.values)[0][1]
    if p > 2.0/3:
        risk = 'high'
    elif p > 1.0/3:
        risk = 'medium'
    else:
        risk = 'low'
    print 'Risk Level: ' + risk + ' with probability of ' + str(p*100) + '%'
    orig['risk_level'] = risk
    orig['fraud_probability'] = p
    return orig.to_json()

def to_database(json_str):
    '''
    Takes in the same json file used to generate our prediction for any 1 event along with the risk_level for that
    event generated by our model. Adds both the input and the output of our model into our SQL database table called
    dataframerequies 'from sqlalchemy import create_engine', along with pandas.

    Input:
        Json_file path(string)
        risk_level(string)
        probability(float)
    Output:
        None
    '''
    df = pd.read_json(json_str)
    del df['ticket_types']
    del df['previous_payouts']

    engine = create_engine('postgresql://William:tiger@10.8.81.53:5432/fraudsters')
    df.to_sql('dataframe', engine,if_exists='append')

if __name__ == '__main__':
    run = raw_input('Run? [y/n] ')
    if run == 'n':
        m = model_load()
        model = m[0]
        dummy_dict = m[1]
        readin = 'example.json'
        point, orig = data_clean(readin, dummy_dict)
        pred_send((point, orig), model)
    # return orig
    else:
        its = int(raw_input('How many iterations? 0 for continuous. '))
        m = model_load()
        model = m[0]
        dummy_dict = m[1]
        if its:
            i = 0
            while i < its:
                j = get_json()
                point, orig = data_cleanJ(j, dummy_dict)
                try:
                    pred = pred_send((point,orig), model)
                    to_database(pred)
                except Exception:
                    pass
                i+=1
                sleep(10)
        else:
            while True:
                j = get_json()
                point, orig = data_cleanJ(j, dummy_dict)
                try:
                    pred = pred_send((point,orig), model)
                    to_database(pred)
                except Exception:
                    pass
                sleep(10)
        # pass
