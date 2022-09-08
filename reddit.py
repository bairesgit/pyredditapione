# python reddit.py
import requests
import json 

subreddit = 'todayilearned'
count = 1
timeframe = 'day' #hour, day, week, month, year, all
listing = 'random' # controversial, best, hot, new, random, rising, top

def get_reddit(subreddit,count):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?count={count}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()

top_post = get_reddit(subreddit,count)

if listing != 'random':
    title = top_post['data']['children'][0]['data']['title']
    url = top_post['data']['children'][0]['data']['url']
else:
    title = top_post[0]['data']['children'][0]['data']['title']
    url = top_post[0]['data']['children'][0]['data']['url']

print(f'{title}\n{url}')
