import oauth2 as oauth
import urllib
import json

CONSUMER_KEY = "B6j7zV3rSYMGatClhRAc2CxxF"
CONSUMER_SECRET = "NO1RNpgmt5BmMThrDMM17gl8lgEiBsenHTJRfng51V6GMujkqi"
ACCESS_KEY = "405679306-T4ZGIgsCO0EyRy699iZ8dSnQwyqwAXPX6pr4g5xB"
ACCESS_SECRET = "PIzjpZW4QJJwTP3ckKpszxegXCyIODo39gj2H5edBF32r"

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

params = {}
params["screen_name"] = 'pgatourmedia'
params["count"] = 200
params["trim_user"] = True

HOLE_LOCATION = 'location'

for page in range(1,11):
    params["page"] = page
    endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    query_string = urllib.urlencode(params)
    url = endpoint+"?"+query_string
    print url
    response, data = client.request(url)
    tweets = json.loads(data)
    for tweet in tweets:
        if HOLE_LOCATION in tweet['text']:
            print tweet['text']
#            print tweet['entities']['user_mentions'][0]['screen_name']
#            print tweet['entities']['media'][0]['media_url_https']
