# coding: utf-8



import requests
import json
import time
import pandas as pd
from tqdm import tqdm


def fetch_channel(query_channel):
    # changing the user-agent 
    headers = {'User-agent': 'E Bot 1.0'}

    # setting after = None so I can start from the first page
    after = None

    # initializing an empty list of posts
    shower_thoughts = []

    # assigning the url
    url = "https://www.reddit.com/r/"+query_channel+"/.json"

    # in order to get around 500 posts, run the loop 20 times
    for i in range(20):

        # print index so I can check that it's proceeding
        print(i)

        # parameters are null for the first page
        if after == None:
            params = {}    
        else:
            # otherwise I have to change the parameter 'after' so it does not start all over again
            params = {'after': after}

        # generating the request  
        res = requests.get(url, params = params, headers = headers)

        # if there are no errors
        if res.status_code == 200:

            # get the json file
            sh_thoughts_json = res.json()

            # extend the list of posts with the children dictionary
            shower_thoughts.extend(sh_thoughts_json['data']['children'])

            # reassign the after parameter so the loop can move to the next set of posts
            after = sh_thoughts_json['data']['after']

        # if there is an error, print the type and break the loop
        else:
            print(res.status_code)
            break

        # 2 seconds break before pinging the server again
        time.sleep(2)
    reddits=[]
    for i in tqdm(shower_thoughts):
        reddits.append(i['data']['title']+i['data']['selftext'])

    # creating the dataframe from the list
    st_df = pd.DataFrame(reddits, columns=['post text'])

    # adding the subreddit column
    st_df['subreddit'] = query_channel

    # checking
    return st_df

dat=fetch_channel('donaldtrump')
print(dat)