from django.shortcuts import render
from django.contrib import messages
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from tweepy import TweepError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Account, Twit
from . import tweeter_credentials
from .forms import UpdateForm, InputPinForm
from tweepy import StreamListener
from tweepy import Stream
import time
from django.core.paginator import Paginator


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

# hash_tag_list = ["donald trump", "hillary clinton"]
# fetched_tweets_filename = "tweets.json"


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list, time_limit):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename, time_limit=time_limit)
        auth = self.twitter_autenticator.authenticate_twitter_app()
        stream = Stream(auth=auth, listener=listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(follow=hash_tag_list, languages=["en"])


### Add list of hashtags and mentions from tweet dictionary ###
def hashtag_to_list(hashtags, mentions):
    list_of_hashtags = []
    for hashtag in hashtags:
        list_of_hashtags.append(hashtag['text'])
    for mention in mentions:
        list_of_hashtags.append(mention['screen_name'])
    return list_of_hashtags


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename, time_limit):
        self.start_time = time.time()
        self.limit = time_limit
        super(TwitterListener, self).__init__()
        self.fetched_tweets_filename = fetched_tweets_filename

    # def on_data(self, data):
    #     try:
    #         print(data)
    #         with open(self.fetched_tweets_filename, 'a') as tf:
    #             tf.write(data)
    #         return True
    #     except BaseException as e:
    #         print("Error on_data %s" % str(e))
    #     return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)

    def on_status(self, status):
        ## Logic of streaming ##
        if status.truncated == True:
            twitter_id = status.id_str
            release_date = status.created_at
            text = status.extended_tweet['full_text']
            hash_tags = hashtag_to_list(status.extended_tweet['entities']['hashtags'],
                                        status.extended_tweet['entities']['user_mentions'])
            twitter_user = status.user.screen_name
            lang = status.lang
        else:
            twitter_id = status.id_str
            release_date = status.created_at
            text = status.text
            hash_tags = hashtag_to_list(status.entities['hashtags'], status.entities['user_mentions'])
            twitter_user = status.user.screen_name
            lang = status.lang
        if not hasattr(status, "retweeted_status") and lang=="en":
            twit_instance = Twit(
                twitter_id=twitter_id,
                twitter_user=twitter_user,
                release_date=release_date,
                text=text,
                hash_tags=hash_tags
                )
            twit_instance.save()

        if (time.time() - self.start_time) > self.limit:
            print('Limit of time is end: ' + str(self.limit) + ' seconds')

            return False








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
    if request.method == 'POST':
        account_name = request.POST['account_name']
        account_id = request.POST['account_id']
        if Account.objects.filter(account=account_name):
            messages.error(request, 'This account has already added to your list')

        else:
            acc_instance = Account(
                account=account_name,
                acc_id=account_id
            )
            acc_instance.save()

            messages.success(request, f'You are successfully add @{account_name}  account to database')
            return HttpResponseRedirect('success')

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
            # Get top 20 popular tweets
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
    if request.method == "GET":
        form = UpdateForm()
        return render(request, 'twitter/Searching_page.html', {'form': form})

    if request.method == "POST":
        ### Set the time limit for updating database ###
        form = UpdateForm(request.POST)
        if form.is_valid():
            time_limit = form.cleaned_data['Number_of_stream']
            list_of_id = []
            all_names = Account.objects.values('acc_id')
            for name in all_names:
                list_of_id.append(name['acc_id'])

            # Authenticate using config.py and connect to Twitter Streaming API.
            hash_tag_list = list_of_id
            fetched_tweets_filename = "tweets.json"

            twitter_streamer = TwitterStreamer()
            twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list, time_limit=time_limit)
            messages.success(request, 'Data are successfully updated')
        else:
            print(form.errors)

        return render(request, 'twitter/Searching_page.html', {'form': form})

def success(request):
    # system_messages = messages.get_messages(request)
    # print(system_messages)
    return render(request, 'twitter/success.html', {})


def get_list(request):
    # form = UpdateForm()
    twitt_messages = []
    ### Represent list with different sorting ###
    if request.method == "GET":

        if request.GET.get('offset'):
            offset = int(request.GET.get('offset'))
        else:
            offset = 0
        if request.GET.get('limit'):
            limit = int(request.GET.get('limit'))
        else:
            limit = 0

        if request.GET.get('hash'):
            filter_words = request.GET['hash']
            if request.GET.get('sort'):
                twitt_messages = list(Twit.objects.filter(hash_tags__icontains=filter_words).order_by('-release_date')[offset:limit].values())
            else:
                twitt_messages = list(Twit.objects.filter(hash_tags__icontains=filter_words)[offset:limit].values())
            # if (twitt_messages.exists() == False) or (filter_words == ''):
            #     messages.info(request, 'There is no message for your search')
        else:
            twitt_messages = list(Twit.objects.all().values())


    return JsonResponse(data=twitt_messages, safe=False)
    # return render(request, 'twitter/Searching_page.html', {'twitt_messages': twitt_messages, 'form': form})



# def start_view(request):

    # consumer_key = tweeter_credentials.CONSUMER_KEY
    # consumer_secret = tweeter_credentials.CONSUMER_SECRET
    # callback_uri = 'oob'
    #
    # # Example using callback (web app)
    # verifier = request.GET.get('oauth_verifier')
    # # Let's say this is a web app, so we need to re-build the auth handler
    # # first...
    # auth = OAuthHandler(consumer_key, consumer_secret, callback_uri)
    # try:
    #     redirect_url = auth.get_authorization_url()
    # except tweepy.TweepError:
    #     print('Error! Failed to get request token.')
    #
    # print(redirect_url)
    # request.session.set('request_token', auth.request_token['oauth_token'])
    # request.session.delete('request_token')
    #
    # auth.request_token = {'oauth_token': token,
    #                       'oauth_token_secret': verifier}
    #
    # try:
    #     auth.get_access_token(verifier)
    # except TweepError:
    #     print('Error! Failed to get access token.')
    # print(auth.access_token, auth.access_token_secret)
    # return HttpResponse('Hi')


## Autorization for web application
def auth(request):
    consumer_key = tweeter_credentials.CONSUMER_KEY
    consumer_secret = tweeter_credentials.CONSUMER_SECRET
    # start the OAuth process, set up a handler with our details
    oauth = OAuthHandler(consumer_key, consumer_secret)
    # direct the user to the authentication url
    # if user is logged-in and authorized then transparently goto the callback URL
    auth_url = oauth.get_authorization_url(True)
    response = HttpResponseRedirect(auth_url)
    # store the request token
    request.session['request_token'] = oauth.request_token
    return response



