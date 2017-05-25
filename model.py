import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score
import cPickle as pickle
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split


#Function to balance classes
def balancer(df, label, margin = 0.4, size = 500):
    yes = df[df[label] == 1]
    no = df[df[label] == 0]
    return yes.sample(int(size * margin),axis =0).append(no.sample(size - int(size * margin),axis =0))

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

#Converting Date columns to datetime objects
datecols = ['approx_payout_date', 'event_created', 'event_end', 'event_start', 'event_published', 'user_created']
convert = lambda x: dt.datetime.fromtimestamp(x)
for i in datecols:
    df[i]=dfi].apply(pd.to_numeric)
    df[i]=df[i].apply(convert)

#Removing time, focus on just the date/day
df['created_date'] = df['event_created'].dt.date
df['started_date'] = df['event_start'].dt.date
df['approx_payout_day'] = df['approx_payout_date'].dt.date

#Creating new column, True when created_date and started_date are the same (more likely to be fraud)
df['all_equal'] = df['created_date'] == df['started_date']
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
    df1 = pd.concat([df1, pd.get_dummies(df[col], prefix = col)], axis=1)
    dummy_vals.append(list(df1[col].unique()))
    df1.pop(col)
dummies = dict(zip(dummy_col, dummy_vals))
# df1.shape


### Classes are imbalanced (90 - 10). Rebalancing the classes to get better model.
df2_bal = balancer(df1, 'Fraud', 0.4, 1000)
print "After training data balance"
print 'Number of True:', df2_bal['Fraud'].sum()
print 'Number of False:', 1000 - df2_bal['Fraud'].sum()
print 'Percentage of False: ', 1 - df2_bal['Fraud'].mean()

#Creating train/test split
y = df2_bal.pop('Fraud').values
X = df2_bal.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33)

#Start training a model!
# Build a forest and compute the feature importances
forest = ExtraTreesClassifier(n_estimators=250,
                              random_state=0)

forest.fit(X_train, y_train)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

feature_list = df2_train.columns.values

# Print the feature ranking
print("Feature ranking:")

for f in range(20):
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

# This time, RandomForestClassifier
# Build the RandomForestClassifier again setting the out of bag parameter to be true
rf = RandomForestClassifier(n_estimators=30, oob_score=True)
rf.fit(X_train, y_train)
print "RF accuracy score:", rf.score(X_test, y_test)
print " out of bag score:", rf.oob_score_

y_predict = rf.predict(X_test)
print precision_score(y_test, y_predict)
print recall_score(y_test, y_predict)
print confusion_matrix(y_test, y_predict)

# Store the model, as well as the dummy variables to work off
pickle.dump((rf, dummies), open('model.p', 'wb'))
