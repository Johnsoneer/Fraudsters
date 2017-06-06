# Fraudsters
Case-study on detecting fraud for an event-hosting webiste. 

This is a group-project invovling four data-science students where we were given a task to create a fraud-detection software package for a 'client' who wanted a web-based app to help them point out which accounts were at high-risk of being fruadulent. Event-hosting websites, such as Eventbrite, might be the unwitting host for credit-card thieves to cash out. These fraudsters could start up a fake event, set a high price for admittance, and use the stolen credit card to buy out all the tickets and send the 'sales' straight to their bank account. 
The challenge was to build a model that could detect when/where these fraudsters were and then build software that our client could easily use to identify who these fraudsters were. 

We ended up splitting the task into three pieces. The predictive model, a SQL database, and a web-based app built on Flask that displayed which events were at high-risk for fraud so the client could investigate further. Each piece was done on a separate computer using an open SQL server so that the other machines could remote-access it to add or query data from it. This way, we could each work in parallel as we built our software. Also, if something needed changing, the other pieces could remain running and in-tact while maintenance could be finished. 

# Results

We created a Random-Forest model to predict the likelyhood of any particular event being classified as fraud. We found our out-of-sample accuracy was 94% and our recall was over 99%. We also found that the most common element for a fraudulent event was when the created-date and the start-date were on the same day. Fraudsters, as it turns out, would try and cash out as quickly as possible, which made them easier for us to find. We were finding, on average, 5 fraudulent events per hour, and since the average fraudulent payout was $1,024, we were saving our client upwards of $5,000 an hour with our model.

Our web-based Flask app was designed to display real-time which current events were at highest risk of fraud. The client could then take that information and follow up with that event and determine if it truly was fraudlent or not. 

For further information on our process, look at the 'Overview.md' file for an in-depth look. 
