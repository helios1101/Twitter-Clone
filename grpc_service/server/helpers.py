from grpc_service.database.twitter_clone_db import TwitterCloneDB  # for tests
from grpc_service.proto.twitter_clone_pb2 import Tweet  # for tests
# from database.twitter_clone_db import TwitterCloneDB  # for grpc_server
# from proto.twitter_clone_pb2 import Tweet  # for grpc_server
from google.protobuf.timestamp_pb2 import Timestamp


class Helper:
    def __init__(self, twitter_clone_db=None):
        self.all_tweets = []
        self.twitter_clone_db = twitter_clone_db or TwitterCloneDB()

    def get_all_tweets(self):
        tweets = self.twitter_clone_db.get_all_tweets()
        t1 = Timestamp()
        t2 = Timestamp()
        for tweet in tweets:
            if tweet.posted_at is not None:
                t1.FromDatetime(tweet.posted_at)
            if tweet.last_edited_at is not None:
                t2.FromDatetime(tweet.last_edited_at)
            else:
                t2 = t1
            ret_tweet = Tweet(
                id=tweet.id,
                username=tweet.username,
                content=tweet.content,
                posted_at=t1,
                last_edited_at=t2,
            )
            for tag in tweet.tags:
                ret_tweet.tag.append(tag.tag)
            self.all_tweets.append(ret_tweet)
        return self.all_tweets

    def get_tweets(self, request):
        tweets = self.twitter_clone_db.get_tweets(request.username)
        t1 = Timestamp()
        t2 = Timestamp()
        for tweet in tweets:
            if tweet.posted_at is not None:
                t1.FromDatetime(tweet.posted_at)
            if tweet.last_edited_at is not None:
                t2.FromDatetime(tweet.last_edited_at)
            else:
                t2 = t1
            ret_tweet = Tweet(
                id=tweet.id,
                username=tweet.username,
                content=tweet.content,
                posted_at=t1,
                last_edited_at=t2,
            )
            for tag in tweet.tags:
                ret_tweet.tag.append(tag.tag)
            self.all_tweets.append(ret_tweet)
        return self.all_tweets

    def create_tweet(self, request):
        response = self.twitter_clone_db.create_tweet(
            request.username, request.content, request.tag
        )
        return response

    def remove_tweet(self, request):
        self.twitter_clone_db.remove_tweet(request.id)

    def edit_tweet(self, request):
        response = self.twitter_clone_db.edit_tweet(
            request.id, request.content, request.tag
        )
        return response
