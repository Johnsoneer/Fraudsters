# Context
The problem we're trying to solved is to get a good idea of which events in an e-commerce website's event list are actually fraudsters using stolen credit-cards to cash out by creating a fake event and buying out all the tickets at a high price. Detecting this kind of fraud could mean the difference between catching a thief or someone loosing their life savings, but our goal is not to predict and act. Rather, we only want to gauge the risk levels of any particular event so that the company can follow up with the high-risk events and decide how to act from there.

# Process
Our inputs are JSON files that describe events registered by users of the website and their relevant information like location, start date, descriptions, and so on. Once our model is built, we will be able to take in individual events and return a risk factor for that particular event based on our training data.

# Data Cleanup and Feature Engineering
After dropping the null values and turning the UNIX datecode columns into dates we can read, we took a look at what features were associated with fraud. A few interesting features we found were the relationship between 'Start_Date' and 'Created_Date'. We found that if we only looked at events that were set to start on the same day they were created, more than 40% of those events were fraudulent! So our model creates a new variable to discover whether that is the case or not for any one event. We also found that the length of the description, the number of channels, and whether or not the event was published to Facebook were all very important factors in predicting a fraudulent event.

![screen shot 2017-05-24 at 5 05 21 pm](https://cloud.githubusercontent.com/assets/24977834/26427659/5d58d4bc-40a3-11e7-81ba-ee4cf8c621de.png)

#Creating and Testing the Model
Simple prediction accuracy is actually not that revealing of a test-metric. Since only around 10% of our cases are labeled as fraud, we could achieve a 90% score simply by labeling everything as not fraud. So along with our out-of-bag score, we also observe recall, which gives us a better understanding of how often we're correctly labeling the fraudulent events.

We tested logistic regression, Random Forests, gradient boosting and Adaboosts. After testing them all on our cleaned dataset, we found that the highest scoring model was a Random Forest classifier that returned us an out-of-bag score of 94% and a recall of .99. We didn't bother refining after that score.

# Further steps

If we had more time, perhaps we might try doing some NLP on the descriptions of each event. We imagine that some fraudsters might be lazy and write descriptions that don't make sense with the listed venue, or perhaps are gibberish.
