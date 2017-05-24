import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score
import cPickle as pickle
import pprint
from itertools import cycle

from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp

df = pd.read_json('data.json')

df['Fraud'] = ((df['acct_type'] == 'fraudster_event') | (df['acct_type'] == 'fraudster') | \
               (df['acct_type'] == 'locked') | (df['acct_type'] == 'tos_lock') | \
               (df['acct_type'] == 'tos_warn') | (df['acct_type'] == 'fraudster_att'))

## Remove rows with null values in these features
df = df[np.isfinite(df['venue_longitude'])]
df = df[np.isfinite(df['event_published'])]
df = df[np.isfinite(df['org_facebook'])]
df = df[np.isfinite(df['sale_duration'])]
df = df.dropna(subset=['country'])
df = df.dropna(subset=['delivery_method'])

#Selecting just the dates
df_copy = df.copy()

datecols = ['approx_payout_date', 'event_created', 'event_end', 'event_start', 'event_published', 'user_created']

convert = lambda x: dt.datetime.fromtimestamp(x)
for i in datecols:
    df_copy[i]=df_copy[i].apply(pd.to_numeric)
    df_copy[i]=df_copy[i].apply(convert)


df_copy['created_date'] = df_copy['event_created'].dt.date
df_copy['started_date'] = df_copy['event_start'].dt.date
# df['published_date'] = df['event_published'].dt.date
df_copy['approx_payout_day'] = df_copy['approx_payout_date'].dt.date
#Creating new column where TRUE if all dates are equal
date_df = df_copy[['Fraud','created_date','started_date']]
date_df['all_equal'] = ((date_df['created_date']==date_df['started_date']))
#(date_df[‘created_date’]==date_df[‘published_date’]) &
# created_started = date_df[date_df['all_equal']==True]
# sum(created_started['Fraud'])/float(len(created_started))
df['all_equal'] = date_df['all_equal']
df1 = df.copy()

## Keep these column in training data as well as lable columne ['Fraud']
# keep_col = ['approx_payout_date', 'all_equal', 'body_length', 'channels', 'country', 'currency', \
#             'delivery_method', 'event_created', 'event_end', 'event_published', 'event_start', \
#             'fb_published', 'gts', 'has_analytics', 'has_logo', 'listed', \
#             'name_length', 'num_order', 'num_payouts', 'org_facebook', 'org_twitter', \
#             'payout_type', 'sale_duration', 'sale_duration2', 'show_map', 'user_age', \
#             'user_created', 'user_type', 'venue_country', 'venue_latitude', 'venue_longitude', \
#             'venue_state', 'Fraud']

keep_col = ['all_equal', 'body_length', 'channels', 'country', 'currency', \
            'delivery_method', 'event_created', 'event_end', 'event_published', 'event_start', \
            'fb_published', 'gts', 'has_analytics', 'has_logo', 'listed', \
            'name_length', 'num_order', 'num_payouts', 'org_facebook', 'org_twitter', \
            'payout_type', 'sale_duration', 'sale_duration2', 'show_map', 'user_age', \
            'user_created', 'user_type', 'venue_country', 'venue_latitude', 'venue_longitude', \
            'venue_state', 'Fraud']
df1 = df1[keep_col]
dummy_col = ['country', 'currency', 'listed', 'payout_type', 'venue_country', 'venue_state']
dummy_vals = []
### Create dummy columns
for col in dummy_col:
    df1 = pd.concat([df1, pd.get_dummies(df[col])], axis=1)
    dummy_vals.append(list(df1[col].unique()))
    del df1[col]
dummies = dict(zip(dummy_col, dummy_vals))
df1.shape

df2_train_True = df2_train[df2_train['Fraud'] == True]
### Balancing traing data
df2_train_False = df2_train[df2_train['Fraud'] == False]
df2_train_False_remove, df2_train_False_keep = train_test_split(df1, test_size = 0.3, random_state = 20)
df2_train_bal = pd.concat((df2_train_True, df2_train_False_keep))

print "After training data balance"
print 'Number of True:', len(df2_train_bal[df2_train_bal['Fraud'] == True])
print 'Number of False:', len(df2_train_bal[df2_train_bal['Fraud'] == False])
print 'Percentage of False: ', round(len(df2_train_bal[df2_train_bal['Fraud'] == False]) / \
                                                float(len(df2_train_bal)), 4) * 100, '%'

y_train = df2_train_bal.pop('Fraud')
x_train = df2_train_bal.values
y_test  = df2_test.pop('Fraud')
x_test  = df2_test.values
y_train = y_train.values.reshape(-1,1)
y_test = y_test.values.reshape(-1,1)

# Build a forest and compute the feature importances
forest = ExtraTreesClassifier(n_estimators=250,
                              random_state=0)

forest.fit(x_train, y_train)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

feature_list = df2_train.columns.values

# Print the feature ranking
print("Feature ranking:")

for f in range(x_train.shape[1]):
    print("%d. feature %d (%f): %s" % (f + 1, indices[f], importances[indices[f]], \
                                       feature_list[f]))

# Plot the feature importances of the forest
mpl_fig = plt.figure(figsize=(10, 8))
ax = mpl_fig.add_subplot(111)
# plt.figure()
ax.set_title("Feature importances", fontsize=18)
ax.bar(range(x_train.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
ax.set_xticks(range(10))
ax.set_xlim([-1, 10])
ax.set_xlabel("Feature", fontsize=18)
ax.set_ylabel("Importance", fontsize=18)
ax.set_xticklabels((feature_list), rotation=45, fontsize=14, ha = 'right')
plt.show()

# Build the RandomForestClassifier again setting the out of bag parameter to be true
rf = RandomForestClassifier(n_estimators=30, oob_score=True)
rf.fit(x_train, y_train)
print "RF accuracy score:", rf.score(x_test, y_test)
print " out of bag score:", rf.oob_score_

y_predict = rf.predict(x_test)
print precision_score(y_test, y_predict)
print recall_score(y_test, y_predict)
print confusion_matrix(y_test, y_predict)

pickle.dump((rf, dummies), open('model.p', 'wb'))
