from django.shortcuts import render
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor

from . import tweeter_credentials




#### Twitter Client ####
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

    def get_last_popular_tweets(self, q, num_tweets):
        last_popular = []
        for tweet in Cursor(self.twitter_client.search, q=q).items(num_tweets):
            last_popular.append(tweet)
        return last_popular

    def search_users(self, q, num_users):
        list_of_users = []
        for tweet in Cursor(self.twitter_client.search_users, q=q).items(num_users):
            list_of_users.append(tweet)
        return list_of_users


#### Twitter Authenticater ####
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(tweeter_credentials.CONSUMER_KEY, tweeter_credentials.CONSUMER_SECRET)
        auth.set_access_token(tweeter_credentials.ACCESS_TOKEN, tweeter_credentials.ACCESS_TOKEN_SECRET)
        return auth



hash_tag_list = ["donald trump", "hillary clinton"]
fetched_tweets_filename = "tweets.json"

# def index(request):
#     if request.GET.get("tag_for_searching"):
#         twitter_account = request.GET["tag_for_searching"]
#         twitter_client = TwitterClient()
#         results = twitter_client.search_users(twitter_account, 3)
#     else:
#         results = None
#
#     return render(request, 'twitter/index.html', {
#         "results": results
#     })

def person_actions(request):
    if request.GET.get("tag_for_searching"):
        hash_for_searching = request.GET["tag_for_searching"]
        timelines_from_req = []
        friendlist_from_req = []



        if request.GET["type_of_searching"] == 'timeline':
            #Get real twitter user from hashtag
            twitter_client = TwitterClient(hash_for_searching)
            object_for_searching = twitter_client.search_users(hash_for_searching, 1)
            if object_for_searching:
                screen_name = object_for_searching[0].screen_name
                #Get timeline if real user was found
                twitter_client = TwitterClient(screen_name)
                timelines_from_req = twitter_client.get_user_timeline_tweets(5)

        elif request.GET["type_of_searching"] == 'friendlist':
            # Get real twitter user from hashtag
            twitter_client = TwitterClient(hash_for_searching)
            object_for_searching = twitter_client.search_users(hash_for_searching, 1)
            if object_for_searching:
                screen_name = object_for_searching[0].screen_name
                #Get friendslist if real user was found
                twitter_client = TwitterClient(screen_name)
                friendlist_from_req = twitter_client.get_friend_list(1)
                print(friendlist_from_req)

        return render(request, 'twitter/tweets_for_acc.html', {'timelines_from_req': timelines_from_req, 'friendlist_from_req': friendlist_from_req})


    return render(request, 'twitter/tweets_for_acc.html', {})
