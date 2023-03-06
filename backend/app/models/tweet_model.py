from sqlmodel import SQLModel, Field, BigInt, Integer, String, DateTime
from typing import Any
from datetime import datetime
from app.models.base_model import SoftDeletableModel

class Tweet(SoftDeletableModel, table=True):
    __tablename__ = "tweets"
    tweet_no: int = Field(primary_key=True, autoincrement=True)
    tweet_id: int = Field(big=True, unsigned=True)
    tweet_text: str
    tweet_author: int = Field(big=True, unsigned=True)
    tweet_created_at: datetime
    tweet_retweet_count: int
    tweet_reply_count: int
    tweet_like_count: int
    tweet_quote_count: int

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Tweet):
            return NotImplemented
        return self.tweet_id == other.tweet_id and \
            self.tweet_retweet_count == other.tweet_retweet_count and \
            self.tweet_reply_count == other.tweet_reply_count and \
            self.tweet_like_count == other.tweet_like_count and \
            self.tweet_quote_count == other.tweet_quote_count