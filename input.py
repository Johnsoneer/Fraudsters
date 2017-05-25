# coding: utf-8
import pandas as pd
import datetime as dt
import cPickle as pickle

def model_load():
    return pickle.load(open('model.p', 'rb'))

def data_clean(readin, dummy_dict):
    point = pd.read_json(readin)
    orig = point.copy()
    datecols = ['approx_payout_date', 'event_created', 'event_end', 'event_start', 'event_published', 'user_created']
    convert = lambda x: dt.datetime.fromtimestamp(x)
    for i in datecols:
        point[i]=point[i].apply(pd.to_numeric)
        point[i]=point[i].apply(convert)

    point['created_date'] = point['event_created'].dt.date
    point['started_date'] = point['event_start'].dt.date
    point['approx_payout_day'] = point['approx_payout_date'].dt.date

    #Creating new column, True when created_date and started_date are the same (more likely to be fraud)
    point['all_equal'] = point['created_date'] == point['started_date']

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

def pred_and_send(data, model, ):

if __name__ == '__main__':
    m = pickle.load(open('model.p', 'rb'))
    model = m[0]
    dummy_dict = m[1]
    readin = 'example.json'
    point = pd.read_json(readin)
    orig = point.copy()
    datecols = ['approx_payout_date', 'event_created', 'event_end', 'event_start', 'event_published', 'user_created']
    df_copy = point.copy()
    convert = lambda x: dt.datetime.fromtimestamp(x)
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
    p = model.predict_proba(point.values)[0][1]
    orig['probability'] =  p
    if p > 2.0/3:
        orig['risk'] = 'high'
    elif p > 1.0/3:
        orig['risk'] = 'medium'
    else:
        orig['risk'] = 'low'
    print orig[['risk', 'probability']]
    # return orig
