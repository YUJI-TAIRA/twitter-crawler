# from sqlmodel import SQLModel, Field
# from typing import Optional, Any
# from datetime import datetime
# from app.models.base_model import SoftDeletableModel
# from app.core.enum import Type


# class Tweet(SQLModel, table=True):
#     __tablename__ = "tweets"
#     tweet_id: int = Field(
#         primary_key=True, big=True, unsigned=True, autoincrement=False
#     )
#     tweet_text: str = Field(max_length=500)
#     tweet_author: int = Field(big=True, unsigned=True)
#     tweet_created_at: datetime
#     tweet_retweet_count: int
#     tweet_reply_count: int
#     tweet_like_count: int
#     tweet_quote_count: int
#     # tweet_type: bool = Field(default=False)
#     tweet_is_reply: Optional[Type] = Field(default=None)
#     deleted_at: Optional[datetime] = Field(default=None)

#     def __eq__(self, other: Any) -> bool:
#         if not isinstance(other, Tweet):
#             return NotImplemented
#         return (
#             self.tweet_id == other.tweet_id
#             and self.tweet_retweet_count == other.tweet_retweet_count
#             and self.tweet_reply_count == other.tweet_reply_count
#             and self.tweet_like_count == other.tweet_like_count
#             and self.tweet_quote_count == other.tweet_quote_count
#         )
