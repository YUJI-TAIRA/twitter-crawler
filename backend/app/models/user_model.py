from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users"
    user_no: int = Field(primary_key=True, autoincrement=True)
    user_id: int = Field(big=True, unsigned=True, unique=True)
    user_username: str = Field(max_length=50)
    user_name: str = Field(max_length=50)
    user_description: str
    user_protected: bool
    user_followers_count: int
    user_following_count: int
    user_tweet_count: int
    user_location: str = Field(max_length=50)
    user_url: str = Field(max_length=100)
    user_profile_image_url: str = Field(max_length=100)
    user_created_at: datetime
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    deleted_at: Optional[datetime] = Field(default=None)