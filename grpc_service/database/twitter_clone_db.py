from . import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import os


class TwitterCloneDB:

    dbuser = os.environ.get("dbuser")
    dbpassword = os.environ.get("dbpassword")
    dbhost = os.environ.get("dbhost")

    def __init__(self, db_session=None):
        if db_session:
            self.session = db_session
        else:
            self.engine = create_engine(
                f"mysql+mysqldb://{self.dbuser}:{self.dbpassword}@{self.dbhost}/Twitter_grpc"
            )
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()

    def get_all_tweets(self):
        all_tweets = (
            self.session.query(models.Tweet)
            .order_by(models.Tweet.last_edited_at.desc())
            .order_by(models.Tweet.posted_at.desc())
            .all()
        )
        return all_tweets

    def get_tweets(self, username):
        tweets = (
            self.session.query(models.Tweet)
            .filter(models.Tweet.username == username)
            .order_by(models.Tweet.last_edited_at.desc())
            .order_by(models.Tweet.posted_at.desc())
            .all()
        )
        return tweets

    def create_tweet(self, username, content, tags):
        tweet_new = models.Tweet(username=username, content=content,)
        for tag in tags:
            tweet_new.tags.append(models.Tag(tag=tag))
        self.session.add(tweet_new)
        self.session.commit()
        return tweet_new

    def remove_tweet(self, id):
        try:
            tweet = self.session.query(models.Tweet).filter(models.Tweet.id == id).one()
            self.session.delete(tweet)
            self.session.commit()
        except NoResultFound:
            return None

    def edit_tweet(self, id, content, tags):
        try:
            tweet = self.session.query(models.Tweet).filter(models.Tweet.id == id).one()
            tweet.content = content
            tags_present = set([tag.tag for tag in tweet.tags])
            for tag in tags:
                if tag not in tags_present:
                    tweet.tags.append(models.Tag(tag=tag))
            for tag in tweet.tags:
                if tag.tag not in tags:
                    tweet.tags.remove(tag)
            self.session.add(tweet)
            self.session.commit()
            edit_tweet = (
                self.session.query(models.Tweet).filter(models.Tweet.id == id).one()
            )
            return edit_tweet
        except NoResultFound:
            return None

    def __del__(self):
        self.session.close()
