# python pushshift.py
# run in jupyter!

import requests
query="seo" #Define Your Query
url = f"https://api.pushshift.io/reddit/search/comment/?q={query}"
request = requests.get(url)
json_response = request.json()
json_response

# Step #1: Create a Function to Call Pushshift AP
def get_pushshift_data(data_type, **kwargs):
    """
    Gets data from the pushshift api.
 
    data_type can be 'comment' or 'submission'
    The rest of the args are interpreted as payload.
 
    Read more: https://github.com/pushshift/api
    """
 
    base_url = f"https://api.pushshift.io/reddit/search/{data_type}/"
    payload = kwargs
    request = requests.get(base_url, params=payload)
    return request.json()
	
# Step #2: Define Your Parameters
data_type="comment"     # give me comments, use "submission" to publish something
query="python"          # Add your query
duration="30d"          # Select the timeframe. Epoch value or Integer + "s,m,h,d" (i.e. "second", "minute", "hour", "day")
size=1000               # maximum 1000 comments
sort_type="score"       # Sort by score (Accepted: "score", "num_comments", "created_utc")
sort="desc"             # sort descending
aggs="subreddit"        #"author", "link_id", "created_utc", "subreddit"

# Step #3: Make the Reddit API Call
get_pushshift_data(data_type=data_type,     
                   q=query,                 
                   after=duration,          
                   size=size,               
                   sort_type=sort_type,
                   sort=sort)
				   
# Step #4: Find in Which Subreddit is Talking More About Your Keyword   
data = get_pushshift_data(data_type=data_type,
                          q=query,
                          after=duration,
                          size=size,
                          aggs=aggs)
						  
#data = data.get("aggs").get(aggs)
				   
# Step #5: Add the Data to a Data Frame
import pandas as pd
df = pd.DataFrame.from_records(data)[0:10]
print(df)

# Step #6: Plot the Data Using Plotly
import plotly.express as px
 
px.bar(df,              # our dataframe
       x="key",         # x will be the 'key' column of the dataframe
       y="doc_count",   # y will be the 'doc_count' column of the dataframe
       title=f'Subreddits with most activity - comments with "{query}" in the last "{duration}"',
       labels={"doc_count": "# comments","key": "Subreddits"}, # the axis names
       color_discrete_sequence=["#1f77b4"], # the colors used
       height=500,
       width=800)
	   
# Step #7: Find the Most Up-Voted Comments	   
# Call the API
data = get_pushshift_data(data_type=data_type,
                          q=query,
                          after="7d",
                          size=10,
                          sort_type=sort_type,
                          sort=sort).get("data")
 
# Select the columns you care about
df = pd.DataFrame.from_records(data)[["author", "subreddit", "score", "body", "permalink"]]
 
# Keep the first 400 characters
df['body'] = df['body'].str[0:400] + "..."
 
# Append the string to all the permalink entries so that we have a link to the comment
df['permalink'] = "https://reddit.com" + df['permalink'].astype(str)
 
 
# Create a function to make the link to be clickable and style the last column
def make_clickable(val):
    """ Makes a pandas column clickable by wrapping it in some html.
    """
    return '<a href="{}">Link</a>'.format(val,val)
 
 
df.style.format({'permalink': make_clickable})











	