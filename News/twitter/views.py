from django.shortcuts import render
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor

from .models import Account, Twit
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

    def get_user(self):
        user_info = self.twitter_client.get_user(id=self.twitter_user)
        return user_info


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
        list_twitter_users = []
        list_of_popular = []

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
            object_for_searching = twitter_client.search_users(hash_for_searching, 10)
            if object_for_searching:
                screen_name = object_for_searching[0].screen_name
                #Get friendslist if real user was found
                twitter_client = TwitterClient(screen_name)
                friendlist_from_req = twitter_client.get_friend_list(1)


        elif request.GET["type_of_searching"] == 'twitter_user':
            # Get the list of twitter_users for the hashtag
            twitter_client = TwitterClient(hash_for_searching)
            object_for_searching = twitter_client.search_users(hash_for_searching, 5)
            list_twitter_users = object_for_searching

        else:
            # Get the top 20 popular tweets
            twitter_client = TwitterClient(hash_for_searching)
            object_for_searching = twitter_client.get_last_popular_tweets(hash_for_searching, 20)
            list_of_popular = object_for_searching

        return render(request, 'twitter/tweets_for_acc.html', {
            'timelines_from_req': timelines_from_req,
            'friendlist_from_req': friendlist_from_req,
            'list_twitter_users': list_twitter_users,
            'list_of_popular': list_of_popular
        })


    return render(request, 'twitter/tweets_for_acc.html', {})


def update_twits(request):
    all_names = Account.objects.values('account')

    #update twits in database
    for name in all_names:
        account_for_searching = name['account']
        all_names = Account.objects.get(account=account_for_searching)

        twitter_client = TwitterClient(account_for_searching)

        timelines_client = twitter_client.get_user_timeline_tweets(3)
        account_info = twitter_client.get_user()
        hash_tag_list = []
        hashtag_for_user = account_info.status.entities['hashtags']
        if hashtag_for_user:
            hash_tag_list.append(hashtag_for_user)

        #add last 3 twits(hashtags, mentions, date, account)
        for timeline in timelines_client:
            list_of_mentions = timeline.entities['user_mentions']

            for mention in list_of_mentions:
                if mention:
                    hash_tag_list.append(mention['screen_name'])

            description = timeline.text
            date_of_public = timeline.created_at
            hash_tags = hash_tag_list

            if request.method == "POST":
                twit_instance = Twit.objects.create(
                     author=all_names,
                     release_date=date_of_public,
                     text=description,
                     hash_tags=hash_tags
                 )
    return render(request, 'twitter/Searching_page.html', {})
