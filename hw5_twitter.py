from requests_oauthlib import OAuth1
import json
# import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time:
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
#username = sys.argv[1]
#num_tweets = sys.argv[2]

username = input("type username")
num_tweets = input("tweets number?")

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this

#Code for Part 1:Get Tweets

base_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

params_dict = {"screen_name": username,
               "count": num_tweets}

response = requests.get(base_url,params_dict,auth=auth)


#code for part 3
cache_fname = "twitter_cache.json"

try:
    cache_file = open(cache_fname, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)


def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(cache_fname,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]
params = {"consumer_key" : secret_data.CONSUMER_KEY,
"consumer_secret" : secret_data.CONSUMER_SECRET,
"access_token" : secret_data.ACCESS_KEY,
"access_secret" : secret_data.ACCESS_SECRET}

cache_finally = make_request_using_cache(base_url, params)
print(cache_finally)

#Code for Part 2:Analyze Tweets
list_of_tweets = json.loads(response.text)

sentence = ""

for tweet in list_of_tweets:
    sentence += tweet["text"]

tokens = nltk.word_tokenize(sentence)

#word_dict = {}
#for i in tokens:
#   if i in word_dict:
#       word_count[i] += 1
#   else:
#       word_count

a = nltk.FreqDist(tokens).items()
b = []
for item in a:
    if item[0] not in ["https", "RT", "http"]:
        if ord(item[0][0]) in range(65,91) or ord(item[0][0]) in range(96,123):
            b.append(item)

b_sorted = sorted(b,key= lambda x:x[1],reverse= True)
print(b_sorted[0:5])



if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
