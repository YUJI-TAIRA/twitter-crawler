from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from sqlmodel import SQLModel, Field

class IncentiveLog(SQLModel):
    __tablename__ = "incentive_logs"
    id: int = Field(primary_key=True, autoincrement=True)
    month: str = Field(max_length=6)
    twitter_id: int = Field(big=True, unsigned=True)
    employee_name: str = Field(max_length=50)
    incentive_total: int
    incentive_like: int
    incentive_follower: int
    incentive_random_lottery: int
    incentive_selection: int
    incentive_best_of_tweet: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("Asia/Tokyo")))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("Asia/Tokyo")))