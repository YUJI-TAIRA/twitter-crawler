from uuid import UUID
from fastapi import APIRouter, Depends
from app.services.twitter_api_v2 import TwitterApiServiceV2

router = APIRouter()


@router.get("/{tweet}")
def get_tweet(
    list_id: str,
) -> list[dict]:
    api = TwitterApiServiceV2()
    tweets = api.get_public_list_timeline(list_id=list_id)

    return tweets
